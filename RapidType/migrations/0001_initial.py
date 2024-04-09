# Generated by Django 5.0.1 on 2024-03-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextPrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('type', models.IntegerField(choices=[(1, 'Normal'), (2, 'Punctuation'), (3, 'Numbers')])),
            ],
        ),
    ]
