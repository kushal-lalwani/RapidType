# Generated by Django 5.0.1 on 2024-03-22 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RapidType', '0003_testresult_test_time_testresult_test_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testresult',
            old_name='test_type',
            new_name='text_type',
        ),
    ]