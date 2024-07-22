# Generated by Django 3.2.25 on 2024-07-21 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_edcp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fondjuridique',
            options={'verbose_name': 'Fondement Juridique', 'verbose_name_plural': 'Fondements Juridique'},
        ),
        migrations.AlterModelOptions(
            name='journaltransaction',
            options={'verbose_name': 'Journal Transaction', 'verbose_name_plural': 'Journals Transactions'},
        ),
        migrations.AlterModelOptions(
            name='persconcernee',
            options={'verbose_name': 'Personne Concernée', 'verbose_name_plural': 'Personnes Concernées'},
        ),
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
