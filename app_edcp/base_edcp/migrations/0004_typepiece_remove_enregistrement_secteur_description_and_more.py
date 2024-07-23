# Generated by Django 4.2.14 on 2024-07-23 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_edcp', '0003_alter_enregistrement_adresse_bp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypePiece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name="Type de pièce d'identité")),
                ('description', models.CharField(max_length=100, null=True, verbose_name='Description du Type de pièce')),
                ('sensible', models.BooleanField(null=True, verbose_name='Est Sensible')),
                ('ordre', models.IntegerField(null=True, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Type de pièce',
                'verbose_name_plural': 'Types de pièces',
            },
        ),
        migrations.RemoveField(
            model_name='enregistrement',
            name='secteur_description',
        ),
        migrations.AddField(
            model_name='enregistrement',
            name='num_piece',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Numéro de la pièce'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='adresse_geo',
            field=models.CharField(max_length=100, null=True, verbose_name='Adresse Géographique'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='effectif',
            field=models.IntegerField(blank=True, null=True, verbose_name='Effectif'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='presentation',
            field=models.CharField(max_length=255, null=True, verbose_name="Présentation de l'activité"),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='raisonsociale',
            field=models.CharField(blank=True, max_length=100, verbose_name='Nom ou raison Sociale'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='rccm',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Numéro RCCM'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='representant',
            field=models.CharField(blank=True, max_length=100, verbose_name='Représentant légal'),
        ),
        migrations.AlterField(
            model_name='enregistrement',
            name='site_web',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Site Web'),
        ),
        migrations.AddField(
            model_name='enregistrement',
            name='type_piece',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='base_edcp.typepiece', verbose_name="Type de pièce d'identité"),
        ),
    ]