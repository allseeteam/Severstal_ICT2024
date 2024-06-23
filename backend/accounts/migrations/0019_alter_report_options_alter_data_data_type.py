# Generated by Django 4.2 on 2024-06-23 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_report_search_end_report_search_start_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('-pk',), 'verbose_name': 'Аналитический отчет', 'verbose_name_plural': 'Аналитические отчеты'},
        ),
        migrations.AlterField(
            model_name='data',
            name='data_type',
            field=models.CharField(choices=[('plotly', 'plotly'), ('text', 'Текст')], verbose_name='Тип данных'),
        ),
    ]