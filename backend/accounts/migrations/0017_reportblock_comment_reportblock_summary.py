# Generated by Django 4.2 on 2024-06-15 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_site_metablock_type_report_template_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportblock',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='reportblock',
            name='summary',
            field=models.TextField(blank=True, verbose_name='Вывод LLM'),
        ),
    ]
