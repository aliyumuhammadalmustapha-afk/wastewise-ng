from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import ScanRecord


class ScanHistoryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='history-user', password='test-password')
        self.client.force_login(self.user)

    def add_scan(self, category, confidence):
        return ScanRecord.objects.create(
            user=self.user,
            image='',
            predicted_class=category,
            confidence_score=confidence,
        )

    def test_filters_category_and_confidence(self):
        matching = self.add_scan('Plastic', 42)
        self.add_scan('Plastic', 82)
        self.add_scan('Glass', 38)

        response = self.client.get(reverse('history'), {'category': 'Plastic', 'confidence': 'low'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['scans']), [matching])
        self.assertEqual(response.context['filtered_count'], 1)

    def test_history_is_paginated(self):
        for index in range(13):
            self.add_scan('Paper', 60 + index)

        response = self.client.get(reverse('history'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['scans']), 12)
        self.assertTrue(response.context['page_obj'].has_next())

    def test_scan_metadata_endpoint_saves_private_scan(self):
        response = self.client.post(reverse('save_scan'), {
            'waste_class': 'Plastic',
            'confidence_score': '94.2',
            'timestamp': timezone.now().isoformat(),
        })

        self.assertEqual(response.status_code, 201)
        saved = ScanRecord.objects.get(pk=response.json()['scan_id'])
        self.assertEqual(saved.predicted_class, 'Plastic')
        self.assertEqual(saved.confidence_score, 94.2)
        self.assertFalse(saved.image)

    def test_scan_metadata_endpoint_rejects_invalid_payload(self):
        response = self.client.post(reverse('save_scan'), {
            'waste_class': 'Unknown',
            'confidence_score': '120',
            'timestamp': 'not-a-timestamp',
        })

        self.assertEqual(response.status_code, 400)

    def test_api_save_scan_json_payload(self):
        import json
        response = self.client.post(
            reverse('api_save_scan'),
            data=json.dumps({
                'waste_class': 'Plastic',
                'specific_item': 'pure_water_sachet',
                'specific_item_name': 'Pure Water Sachet',
                'confidence': 96.8,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        saved = ScanRecord.objects.get(pk=response.json()['scan_id'])
        self.assertEqual(saved.predicted_class, 'Plastic')
        self.assertEqual(saved.confidence_score, 96.8)
        self.assertEqual(saved.specific_item, 'pure_water_sachet')
        self.assertEqual(saved.specific_item_name, 'Pure Water Sachet')

        from .models import Scan
        scan_entry = Scan.objects.filter(user=self.user).first()
        self.assertIsNotNone(scan_entry)
        self.assertEqual(scan_entry.specific_item, 'pure_water_sachet')
        self.assertEqual(scan_entry.specific_item_name, 'Pure Water Sachet')


class WorkspaceTemplateTests(TestCase):
    def test_public_templates_render(self):
        client = Client()
        for route in ('home', 'education', 'login', 'register'):
            with self.subTest(route=route):
                self.assertEqual(client.get(reverse(route)).status_code, 200)

    def test_user_and_admin_templates_render(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(username='template-user', password='test-password')
        client = Client()
        client.force_login(user)
        for route in ('scan', 'dashboard', 'history'):
            with self.subTest(route=route):
                self.assertEqual(client.get(reverse(route)).status_code, 200)

        scan = ScanRecord.objects.create(user=user, image='', predicted_class='Plastic', confidence_score=88.5)
        self.assertEqual(client.get(reverse('result', args=[scan.id])).status_code, 200)

        admin = user_model.objects.create_user(username='template-admin', password='test-password', role='admin')
        client.force_login(admin)
        self.assertEqual(client.get(reverse('admin_dashboard')).status_code, 200)


class AuthenticationAndRecoveryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='khalifa',
            email='khalifa@wastewiseng.org',
            password='ComplexPassword123!'
        )

    def test_login_with_username(self):
        response = self.client.post(reverse('login'), {
            'username': 'khalifa',
            'password': 'ComplexPassword123!'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_with_email(self):
        response = self.client.post(reverse('login'), {
            'username': 'khalifa@wastewiseng.org',
            'password': 'ComplexPassword123!'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_case_insensitive(self):
        response = self.client.post(reverse('login'), {
            'username': 'Khalifa@WasteWiseNG.Org',
            'password': 'ComplexPassword123!'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_password_reset_views_render(self):
        # 1. Reset Form
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reset your password')

        # 2. Reset POST
        post_response = self.client.post(reverse('password_reset'), {
            'email': 'khalifa@wastewiseng.org'
        })
        self.assertRedirects(post_response, reverse('password_reset_done'))

        # 3. Reset Done
        done_response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(done_response.status_code, 200)
        self.assertContains(done_response, 'Check your email')

        # 4. Reset Complete
        complete_response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(complete_response.status_code, 200)
        self.assertContains(complete_response, 'Password Reset Complete')

