# Generated by Django 3.2.25 on 2024-07-10 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_edcp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CasExemption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casexemption', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CategorieDCP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoriedcp', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='CategorieTrait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name='Nom du Pays')),
            ],
            options={
                'verbose_name': 'Pays',
                'verbose_name_plural': 'Pays',
            },
        ),
    ]
