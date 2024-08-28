# Generated by Django 4.2.14 on 2024-08-22 14:12

import base_edcp.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('demande', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base_edcp', '0001_initial'),
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
                ('demande_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='demande.demande')),
                ('moyens_materiels', models.CharField(blank=True, max_length=255, null=True, verbose_name='Moyens matériels mis à la disposition du Correspondant')),
                ('moyens_humains', models.CharField(blank=True, max_length=255, null=True, verbose_name='Moyens humains mis à la disposition du Correspondant')),
                ('experiences', models.TextField(blank=True, null=True, verbose_name='Experiences et diplômes')),
                ('profile_completed', models.BooleanField(default=False, verbose_name='Profil complet')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Approuvé')),
                ('is_rejected', models.BooleanField(default=False, verbose_name='Refusé')),
                ('file_lettre_designation', models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.', null=True, upload_to='docs/correspondant', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])], verbose_name='Lettre de désignation')),
                ('file_lettre_acceptation', models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.', null=True, upload_to='docs/correspondant', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])], verbose_name="Lettre d'acceptation")),
                ('file_attestation_travail', models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.', null=True, upload_to='docs/correspondant', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])], verbose_name='Attestation de travail')),
                ('file_casier_judiciaire', models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.', null=True, upload_to='docs/correspondant', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])], verbose_name='Casier judiciaire')),
                ('file_certificat_nationalite', models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.', null=True, upload_to='docs/correspondant', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])], verbose_name='Certificat de nationalité')),
                ('file_cv', models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.', null=True, upload_to='docs/correspondant', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])], verbose_name='CV')),
                ('exercice_activite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='correspondant.exerciceactivite', verbose_name="Exercice de l'activité")),
                ('qualifications', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='correspondant.qualificationsdpo', verbose_name='Qualifications du Correspondant')),
                ('type_dpo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='correspondant.typedpo', verbose_name='Type de Correspondant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correspondant_profiles', to=settings.AUTH_USER_MODEL, verbose_name='Compte utilisateur')),
            ],
            options={
                'verbose_name': 'Correspondant à la protection des données',
                'verbose_name_plural': 'Correspondants à la protection des données',
            },
            bases=('demande.demande',),
        ),
    ]
