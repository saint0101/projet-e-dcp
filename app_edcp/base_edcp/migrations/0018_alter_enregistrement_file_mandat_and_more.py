# Generated by Django 4.2.14 on 2024-08-05 15:10

import base_edcp.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_edcp', '0017_alter_enregistrement_file_mandat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enregistrement',
            name='file_mandat',
            field=models.FileField(blank=True, help_text="Si vous n'êtes pas le représentant légal, Joindre un mandat signé par le représentatnt légal de l'organisation", null=True, upload_to='docs/enregistrement', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf,jpg,jpeg,png'])], verbose_name='Mandat de représentation'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='file_piece',
            field=models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.', null=True, upload_to='docs/enregistrement', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf,jpg,jpeg,png'])], verbose_name="Pièce d'identité"),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='file_rccm',
            field=models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.', null=True, upload_to='docs/enregistrement', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf,jpg,jpeg,png'])], verbose_name='Copie du Registre du Commerce'),
        ),
    ]
