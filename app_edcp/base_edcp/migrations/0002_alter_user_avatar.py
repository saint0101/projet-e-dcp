# Generated by Django 4.2.14 on 2024-07-31 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_edcp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='uploads/avatars', verbose_name='Avatar'),
        ),
    ]