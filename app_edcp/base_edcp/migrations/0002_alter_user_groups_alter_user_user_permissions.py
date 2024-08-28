# Generated by Django 4.2.14 on 2024-08-12 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base_edcp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='Les groupes auxquels cet utilisateur appartient.', related_name='base_edcp_user_set', to='auth.group', verbose_name='Groupes'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Permissions spécifiques pour cet utilisateur.', related_name='base_edcp_user_permissions_set', to='auth.permission', verbose_name='Permissions des utilisateurs'),
        ),
    ]
