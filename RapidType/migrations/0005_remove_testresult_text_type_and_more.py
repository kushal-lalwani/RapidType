# Generated by Django 5.0.1 on 2024-03-22 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RapidType', '0004_rename_test_type_testresult_text_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='text_type',
        ),
        migrations.AlterField(
            model_name='testresult',
            name='test_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RapidType.userprofile'),
        ),
    ]