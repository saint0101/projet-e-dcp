# Generated by Django 4.2.14 on 2024-07-19 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_edcp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='login',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=100, verbose_name="Nom d'utilisateur"),
        ),
    ]