# Generated by Django 4.2.14 on 2024-09-13 11:27

import base_edcp.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('options', '0001_initial'),
        ('demande', '0002_categoriedemande_montant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Date d'émission")),
                ('montant', models.BigIntegerField(default=0, verbose_name='Montant de la facture')),
                ('restant', models.BigIntegerField(default=0, verbose_name='Reste à payer')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Est payée')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='facture_created', to=settings.AUTH_USER_MODEL, verbose_name='Créateur de la facture')),
                ('demande', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='demande.demande', verbose_name='Demande facturée')),
                ('statut', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='options.status', verbose_name='Statut de la facture')),
            ],
        ),
        migrations.CreateModel(
            name='ModePaiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Codification du champ, à écrire sous forme de slug', max_length=100, unique=True, verbose_name='Label')),
                ('is_sensible', models.BooleanField(default=False, verbose_name='Sensible ?')),
                ('description', models.CharField(blank=True, help_text='Description du champ, affichée sur les formulaire', max_length=255, null=True, verbose_name='Description du champ')),
                ('resume', models.TextField(blank=True, help_text='Paragraphe plus long que la description fournissant des détails sur le champ', max_length=500, null=True, verbose_name='Résumé du champ (texte explicatif)')),
                ('ordre', models.IntegerField(default=0, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Mode de paiement',
                'verbose_name_plural': 'Modes de paiement',
            },
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de paiement')),
                ('montant', models.BigIntegerField(default=0, verbose_name='Montant du paiement')),
                ('is_valid', models.BooleanField(default=False, verbose_name='Est valide')),
                ('file_justificatif', models.FileField(blank=True, help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.', null=True, upload_to='docs/facturation', validators=[base_edcp.validators.validate_files, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])], verbose_name='Justificatif de paiement')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='paiement_created', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur effectuant le paiement')),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facturation.facture', verbose_name='Facture')),
                ('mode_paiement', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='facturation.modepaiement', verbose_name='Mode de paiement')),
            ],
        ),
    ]
