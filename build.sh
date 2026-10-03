#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
cd backend

python manage.py collectstatic --no-input
python manage.py migrate

# Download ML model from Google Drive if not already present
MODEL_PATH="ml_model/wastewise_model.keras"
GDRIVE_FILE_ID="1wFGyiCBS2JilypI3QvX0uYcWf4TxC2uf"

if [ ! -f "$MODEL_PATH" ]; then
    echo "==> Downloading ML model from Google Drive..."
    mkdir -p ml_model
    python -c "
import gdown
gdown.download(id='$GDRIVE_FILE_ID', output='$MODEL_PATH', quiet=False, fuzzy=True)
print('Model downloaded successfully.')
"
else
    echo "==> ML model already exists, skipping download."
fi

# Auto-create superuser from environment variables (only if DJANGO_SUPERUSER_USERNAME is set)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser \
        --no-input \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
        2>/dev/null || echo "Superuser already exists, skipping."
fi

# Ensure all superusers and staff have role='admin'
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
count = User.objects.filter(is_superuser=True).update(role='admin')
print(f'==> Updated {count} superuser(s) with role=admin')
"

