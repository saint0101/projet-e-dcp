# Generated by Django 4.2.14 on 2024-08-01 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base_edcp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciceActivite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': "Mode d'exercice de l'activité",
                'verbose_name_plural': "Modes d'exercice de l'activité",
            },
        ),
        migrations.CreateModel(
            name='QualificationsDPO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Description du Type de Correspondant')),
            ],
            options={
                'verbose_name': 'Qualifications du Correspondant',
            },
        ),
        migrations.CreateModel(
            name='TypeDPO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Description du Type de Correspondant')),
            ],
            options={
                'verbose_name': 'Type de Correspondant',
                'verbose_name_plural': 'Types de Correspondant',
            },
        ),
        migrations.CreateModel(
            name='Correspondant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de désignation')),
                ('moyens_materiels', models.CharField(blank=True, max_length=255, null=True, verbose_name='Moyens matériels mis à la disposition du Correspondant')),
                ('moyens_humains', models.CharField(blank=True, max_length=255, null=True, verbose_name='Moyens humains mis à la disposition du Correspondant')),
                ('experiences', models.TextField(blank=True, null=True, verbose_name='Experiences et diplômes')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Approuvé')),
                ('created_by', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created', to=settings.AUTH_USER_MODEL, verbose_name='Crée par')),
                ('exercice_activite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='correspondant.exerciceactivite', verbose_name="Exercice de l'activité")),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_edcp.enregistrement', verbose_name='Organisation')),
                ('qualifications', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='correspondant.qualificationsdpo', verbose_name='Qualifications du Correspondant')),
                ('type_dpo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='correspondant.typedpo', verbose_name='Type de Correspondant')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='correspondant_user', to=settings.AUTH_USER_MODEL, verbose_name='Compte utilisateur')),
            ],
            options={
                'verbose_name': 'Correspondant à la protection des données',
                'verbose_name_plural': 'Correspondants à la protection des données',
            },
        ),
    ]
