# Generated by Django 4.2 on 2024-06-15 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_reportblock_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(verbose_name='Домен')),
            ],
            options={
                'verbose_name': 'Проверенный сайт',
                'verbose_name_plural': 'Проверенные сайты',
            },
        ),
        migrations.AddField(
            model_name='metablock',
            name='type',
            field=models.CharField(choices=[('plotly', 'Plotly'), ('text', 'Текст')], default='plotly', verbose_name='Тип'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.template', verbose_name='Шаблон'),
        ),
        migrations.AlterField(
            model_name='reportblock',
            name='type',
            field=models.CharField(choices=[('plotly', 'Plotly'), ('text', 'Текст')], verbose_name='Тип'),
        ),
    ]
