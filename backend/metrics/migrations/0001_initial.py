# Generated by Django 4.0.5 on 2022-07-01 15:43

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('device_id', models.UUIDField(verbose_name='Dispositivo')),
                ('metric', models.IntegerField(verbose_name='Metrica')),
                ('report', models.DateTimeField(verbose_name='Fecha de reporte')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
