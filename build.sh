#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
cd backend
python manage.py collectstatic --no-input
python manage.py migrate

# Auto-create superuser from environment variables (only if DJANGO_SUPERUSER_USERNAME is set)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser \
        --no-input \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
        2>/dev/null || echo "Superuser already exists, skipping."
fi
