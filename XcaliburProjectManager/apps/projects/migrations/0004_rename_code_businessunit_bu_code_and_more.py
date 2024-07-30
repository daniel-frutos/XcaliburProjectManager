# Generated by Django 5.0.1 on 2024-07-22 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_businessunit_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businessunit',
            old_name='code',
            new_name='bu_code',
        ),
        migrations.RenameField(
            model_name='businessunit',
            old_name='name',
            new_name='bu_name',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='code',
            new_name='dep_code',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='name',
            new_name='dep_name',
        ),
    ]
