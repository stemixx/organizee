#!/bin/bash

# Создаём файл миграции изменения example.com на 127.0.0.1:8000
cat <<EOF > /usr/src/app/organizee/migrations/0002_initial_site.py
from django.db import migrations


def add_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    site = Site.objects.get(name='example.com')
    site.name = 'localhost'
    site.domain = '127.0.0.1:8000'
    site.save()


class Migration(migrations.Migration):
    dependencies = [
        ('organizee', '0001_initial')
    ]

    operations = [
        migrations.RunPython(add_site),
    ]

EOF
# Выполняем миграцию
python manage.py migrate