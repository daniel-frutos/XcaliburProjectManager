# Generated by Django 5.0.1 on 2024-07-29 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_remove_project_ftem_remove_project_ftg_grav_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='business_units',
            field=models.CharField(blank=True, default=None, max_length=150, null=True),
        ),
    ]