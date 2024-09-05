# Generated by Django 5.1 on 2024-09-04 14:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ozonorder',
            name='acquiring_price',
        ),
        migrations.RemoveField(
            model_name='ozonorder',
            name='cancel_price',
        ),
        migrations.RemoveField(
            model_name='ozonorder',
            name='id',
        ),
        migrations.AddField(
            model_name='ozonorder',
            name='posting_number',
            field=models.CharField(default='unknown', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ozonorder',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ozonorder',
            name='order_id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ozonorder',
            name='order_number',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='ozonorder',
            name='schema',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='ozonorder',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
