# Generated by Django 5.2 on 2025-04-24 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userprofile_plaid_access_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='plaid_access_token',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='access_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
