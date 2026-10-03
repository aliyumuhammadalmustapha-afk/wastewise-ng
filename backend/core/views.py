import json
from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm
from .models import ScanRecord, Scan
from .waste_info import WASTE_INFO
from .ml_model import classify_waste

NIGERIAN_SPECIFIC_ITEMS = {
    'pure_water_sachet', 'nylon_bag', 'ghana_must_go', 'tomato_tin', 'milk_tin',
    'milo_tin', 'beer_bottle', 'soft_drink_bottle', 'gin_bottle', 'newspaper',
    'food_wrap_paper', 'cassava_peel', 'yam_peel', 'palm_kernel',
    'rechargeable_lantern', 'inverter_battery', 'ankara_fabric', 'okrika',
    'head_tie', 'pesticide_container', 'engine_oil_can', 'kerosene_can', 'styrofoam',
}

def home_view(request):
    category_icons = {
        'E-Waste': 'cpu', 'General': 'trash-2', 'Glass': 'wine',
        'Hazardous': 'alert-triangle', 'Metal': 'cylinder', 'Organic': 'leaf',
        'Paper': 'file-text', 'Plastic': 'package', 'Textile': 'scissors'
    }
    return render(request, 'home.html', {
        'platform_scans': ScanRecord.objects.count(),
        'waste_category_count': len(ScanRecord.WASTE_CLASSES),
        'waste_classes': [
            {'name': name, 'label': label, 'icon': category_icons.get(name, 'package')}
            for name, label in ScanRecord.WASTE_CLASSES
        ],
    })

def register_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if (request.user.role == 'admin' or request.user.is_superuser or request.user.is_staff) else 'dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if (request.user.role == 'admin' or request.user.is_superuser or request.user.is_staff) else 'dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard' if (user.role == 'admin' or user.is_superuser or user.is_staff) else 'dashboard')
    else:
        form = AuthenticationForm()
    for name, field in form.fields.items():
        field.widget.attrs.update({'class': 'ww-input', 'autocomplete': 'username' if name == 'username' else 'current-password'})
    return render(request, 'login.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def scan_view(request):
    if request.method == 'POST':
        image = request.FILES.get('waste_image')
        predicted_class = request.POST.get('predicted_class')
        try:
            confidence = float(request.POST.get('confidence_score', ''))
        except (TypeError, ValueError):
            confidence = -1

        allowed_classes = dict(ScanRecord.WASTE_CLASSES)
        if not image or predicted_class not in allowed_classes or not 0 <= confidence <= 100:
            return render(request, 'scan.html', {
                'error': 'Choose an image and run the classifier before saving the scan.',
                'waste_info': WASTE_INFO,
            }, status=400)

        scan_record = ScanRecord.objects.create(
            user=request.user,
            image=image,
            predicted_class=predicted_class,
            confidence_score=round(confidence, 1),
            specific_item=request.POST.get('specific_item', '').strip() or None,
            specific_item_name=request.POST.get('specific_item_name', '').strip() or None,
        )
        return redirect('result', scan_id=scan_record.id)

    return render(request, 'scan.html', {'waste_info': WASTE_INFO})

@require_POST
def api_save_scan(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required. Please log in.'}, status=401)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
        data = request.POST

    waste_class = data.get('waste_class') or data.get('class') or data.get('predicted_class') or ''
    specific_item = data.get('specific_item', '') or ''
    specific_item_name = data.get('specific_item_name', '') or ''
    try:
        confidence = float(data.get('confidence', data.get('confidence_score', -1)))
    except (TypeError, ValueError):
        confidence = -1

    allowed_classes = dict(ScanRecord.WASTE_CLASSES)
    if waste_class not in allowed_classes or not 0 <= confidence <= 100:
        return JsonResponse({'error': 'The scan details are incomplete or invalid.'}, status=400)

    scan = ScanRecord.objects.create(
        user=request.user,
        predicted_class=waste_class,
        confidence_score=round(confidence, 1),
        specific_item=specific_item or None,
        specific_item_name=specific_item_name or None,
    )

    # Mirror entry in legacy Scan model
    class_names = [name for name, _label in ScanRecord.WASTE_CLASSES]
    predicted_index = class_names.index(waste_class) if waste_class in class_names else 0
    Scan.objects.create(
        user=request.user,
        waste_class=waste_class,
        confidence=round(confidence, 1),
        predicted_index=predicted_index,
        specific_item=specific_item or None,
        specific_item_name=specific_item_name or None,
    )

    return JsonResponse({
        'status': 'success',
        'scan_id': scan.pk,
        'created_at': scan.created_at.isoformat(),
        'result_url': reverse('result', args=[scan.pk]),
    }, status=201)

@login_required
@require_POST
def save_scan_view(request):
    return api_save_scan(request)

@login_required
def result_view(request, scan_id):
    try:
        scan = ScanRecord.objects.get(id=scan_id, user=request.user)
    except ScanRecord.DoesNotExist:
        return redirect('history')
        
    info = WASTE_INFO.get(scan.predicted_class, WASTE_INFO['General'])
    return render(request, 'result.html', {
        'scan': scan,
        'info': info,
        'is_nigerian_item': scan.specific_item in NIGERIAN_SPECIFIC_ITEMS,
    })

@login_required
def history_view(request):
    queryset = ScanRecord.objects.filter(user=request.user)
    total_scans = queryset.count()

    # Category filter
    selected_category = request.GET.get('category', '')
    if selected_category:
        queryset = queryset.filter(predicted_class=selected_category)

    # Confidence filter
    selected_confidence = request.GET.get('confidence', '')
    if selected_confidence == 'high':
        queryset = queryset.filter(confidence_score__gte=80)
    elif selected_confidence == 'medium':
        queryset = queryset.filter(confidence_score__gte=50, confidence_score__lt=80)
    elif selected_confidence == 'low':
        queryset = queryset.filter(confidence_score__lt=50)

    filtered_count = queryset.count()

    # Ordering
    selected_ordering = request.GET.get('ordering', 'newest')
    if selected_ordering == 'oldest':
        queryset = queryset.order_by('created_at')
    elif selected_ordering == 'confidence':
        queryset = queryset.order_by('-confidence_score')
    else:
        queryset = queryset.order_by('-created_at')

    # Pagination
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    scans_list = list(page_obj)
    for scan in scans_list:
        scan.danger_level = WASTE_INFO.get(scan.predicted_class, WASTE_INFO['General'])['danger']

    return render(request, 'history.html', {
        'scans': scans_list,
        'page_obj': page_obj,
        'total_scans': total_scans,
        'filtered_count': filtered_count,
        'selected_category': selected_category,
        'selected_confidence': selected_confidence,
        'selected_ordering': selected_ordering,
        'waste_classes': ScanRecord.WASTE_CLASSES,
    })

@login_required
def dashboard_view(request):
    scans = ScanRecord.objects.filter(user=request.user)
    category_data = scans.values('predicted_class').annotate(count=Count('id')).order_by('predicted_class')
    categories = list(category_data)
    most_common = max(categories, key=lambda item: item['count']) if categories else None
    today = timezone.localdate()
    since = today - timedelta(days=6)
    activity = {
        item['day'].isoformat(): item['count']
        for item in scans.filter(created_at__date__gte=since).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id'))
    }
    activity_days = [since + timedelta(days=offset) for offset in range(7)]
    recent_scans = list(scans.order_by('-created_at')[:5])
    for scan in recent_scans:
        scan.danger_level = WASTE_INFO.get(scan.predicted_class, WASTE_INFO['General'])['danger']
    context = {
        'total_scans': scans.count(),
        'most_common': most_common['predicted_class'] if most_common else 'No scans yet',
        'recyclable_scans': scans.filter(predicted_class__in=['Plastic', 'Metal', 'Glass', 'Paper']).count(),
        'hazardous_scans': scans.filter(predicted_class='Hazardous').count(),
        'category_labels': [item['predicted_class'] for item in categories],
        'category_counts': [item['count'] for item in categories],
        'activity_labels': [day.strftime('%a') for day in activity_days],
        'activity_counts': [activity.get(day.isoformat(), 0) for day in activity_days],
        'recent_scans': recent_scans,
    }
    return render(request, 'user_dashboard.html', context)

def education_view(request):
    icons = {
        'E-Waste': 'cpu', 'General': 'trash-2', 'Glass': 'wine',
        'Hazardous': 'alert-triangle', 'Metal': 'cylinder', 'Organic': 'leaf',
        'Paper': 'file-text', 'Plastic': 'package', 'Textile': 'scissors'
    }
    materials = []
    for name, _label in ScanRecord.WASTE_CLASSES:
        info = WASTE_INFO[name]
        materials.append({**info, 'name': name, 'icon': icons.get(name, 'package'), 'guidance': info['disposal']})
    return render(request, 'education.html', {'materials': materials})

def about_view(request):
    return redirect('home')

def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser or user.is_staff)

@user_passes_test(is_admin, login_url='home')
def admin_dashboard_view(request):
    User = get_user_model()
    total_scans = ScanRecord.objects.count()
    scans = ScanRecord.objects.select_related('user').order_by('-created_at')
    recent_scans = list(scans[:50])
    for scan in recent_scans:
        scan.danger_level = WASTE_INFO.get(scan.predicted_class, WASTE_INFO['General'])['danger']
    category_data = list(ScanRecord.objects.values('predicted_class').annotate(count=Count('id')).order_by('-count'))
    today = timezone.localdate()
    since = today - timedelta(days=6)
    activity = {
        item['day'].isoformat(): item['count']
        for item in scans.filter(created_at__date__gte=since).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id'))
    }
    activity_days = [since + timedelta(days=offset) for offset in range(7)]
    users = list(User.objects.annotate(scan_count=Count('scan_records')).order_by('-date_joined')[:20])
    context = {
        'total_scans': total_scans,
        'total_users': User.objects.count(),
        'most_classified': category_data[0]['predicted_class'] if category_data else 'No scans yet',
        'hazardous_scans': ScanRecord.objects.filter(predicted_class='Hazardous').count(),
        'total_classified_categories': len(category_data),
        'recent_scans': recent_scans,
        'users': users,
        'scan_headings': ['User', 'Waste Type', 'Specific Item', 'Confidence', 'Date'],
        'chart_labels': [item['predicted_class'] for item in category_data],
        'chart_counts': [item['count'] for item in category_data],
        'activity_labels': [day.strftime('%a') for day in activity_days],
        'activity_counts': [activity.get(day.isoformat(), 0) for day in activity_days],
    }
    return render(request, 'admin_dashboard.html', context)

def classify_image(request):
    """Classify an uploaded waste image and return JSON."""
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'POST method required.'}, status=405)
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required. Please log in.'}, status=401)
        if 'image' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No image provided.'}, status=400)
        
        image_file = request.FILES['image']
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
        if image_file.content_type not in allowed_types:
            return JsonResponse({'success': False, 'error': 'Invalid file type. JPG, PNG and WebP supported.'}, status=400)
        
        result = classify_waste(image_file)
        if not result.get('success'):
            return JsonResponse({'success': False, 'error': result.get('error', 'Classification failed.')}, status=200)
        return JsonResponse(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': f'Server error during classification: {str(e)}'}, status=200)

