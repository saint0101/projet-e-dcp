# Generated by Django 4.2.14 on 2024-08-05 14:50

import base_edcp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_edcp', '0015_enregistrement_idu_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enregistrement',
            name='adresse_geo',
            field=models.CharField(max_length=100, null=True, validators=[base_edcp.validators.validate_charfield, base_edcp.validators.validate_no_special_chars], verbose_name='Adresse Géographique'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='email_contact',
            field=models.EmailField(max_length=100, null=True, verbose_name='Email de Contact'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='file_piece',
            field=models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 10 Mb.', null=True, upload_to='docs/enregistrement', verbose_name="Pièce d'identité"),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='file_rccm',
            field=models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 10 Mb.', null=True, upload_to='docs/enregistrement', verbose_name='Copie du Registre du Commerce'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='raisonsociale',
            field=models.CharField(blank=True, help_text="Nom de la personne physique ou de l'organisation à enregistrer", max_length=100, validators=[base_edcp.validators.validate_charfield, base_edcp.validators.validate_no_special_chars], verbose_name='Nom ou Raison Sociale'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='rccm',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[base_edcp.validators.validate_charfield, base_edcp.validators.validate_no_special_chars, base_edcp.validators.validate_rccm_idu], verbose_name='Numéro RCCM'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='representant',
            field=models.CharField(blank=True, max_length=100, verbose_name='Nom du représentant légal'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='telephone',
            field=models.CharField(max_length=20, null=True, validators=[base_edcp.validators.validate_phone_number], verbose_name='Téléphone'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='ville',
            field=models.CharField(max_length=100, null=True, validators=[base_edcp.validators.validate_charfield, base_edcp.validators.validate_no_special_chars], verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fonction',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[base_edcp.validators.validate_charfield, base_edcp.validators.validate_no_special_chars], verbose_name='Fonction'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nom',
            field=models.CharField(max_length=225, validators=[base_edcp.validators.validate_charfield, base_edcp.validators.validate_no_special_chars], verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='user',
            name='organisation',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[base_edcp.validators.validate_charfield, base_edcp.validators.validate_no_special_chars], verbose_name='Organisation'),
        ),
        migrations.AlterField(
            model_name='user',
            name='prenoms',
            field=models.CharField(max_length=255, validators=[base_edcp.validators.validate_charfield, base_edcp.validators.validate_no_special_chars], verbose_name='Prénoms'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[base_edcp.validators.validate_charfield, base_edcp.validators.validate_no_special_chars], verbose_name='Téléphone'),
        ),
    ]