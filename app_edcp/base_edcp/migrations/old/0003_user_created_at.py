# Generated by Django 4.2.14 on 2024-07-24 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_edcp', '0002_enregistrement_has_dpo_user_is_dpo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date de Création'),
        ),
    ]
