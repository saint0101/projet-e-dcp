# Generated by Django 4.2.14 on 2024-09-13 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demande', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoriedemande',
            name='montant',
            field=models.BigIntegerField(default=0, verbose_name='Montant à payer'),
        ),
    ]