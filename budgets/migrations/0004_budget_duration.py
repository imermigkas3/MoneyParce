# Generated by Django 5.0 on 2025-04-22 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0003_alter_budget_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='duration',
            field=models.CharField(blank=True, help_text='weekly, monthly, annually', max_length=50),
        ),
    ]
