# Generated by Django 4.2 on 2024-06-11 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_report_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportblock',
            name='representation',
            field=models.JSONField(default={}, verbose_name='Представление'),
            preserve_default=False,
        ),
    ]