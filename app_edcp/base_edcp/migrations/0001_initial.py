# Generated by Django 4.2.14 on 2024-07-24 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date de Création')),
                ('username', models.CharField(blank=True, max_length=100, verbose_name="Nom d'utilisateur")),
                ('avatar', models.FileField(blank=True, max_length=255, null=True, upload_to='avatars/', verbose_name='Avatar')),
                ('nom', models.CharField(max_length=225, verbose_name='Nom')),
                ('prenoms', models.CharField(max_length=255, verbose_name='Prénoms')),
                ('organisation', models.CharField(blank=True, max_length=255, null=True, verbose_name='Organisation')),
                ('telephone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Téléphone')),
                ('fonction', models.CharField(blank=True, max_length=255, null=True, verbose_name='Fonction')),
                ('consentement', models.CharField(blank=True, max_length=255, null=True, verbose_name='Consentement')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=True, verbose_name='Est Actif')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Est Membre du Personnel')),
                ('email_verified', models.BooleanField(default=False)),
                ('is_dpo', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateurs',
            },
        ),
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
            name='Finalite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('sensible', models.CharField(max_length=100)),
                ('ordre', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Fonction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fonction', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FondJuridique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Fondement Juridique',
                'verbose_name_plural': 'Fondements Juridique',
            },
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
        migrations.CreateModel(
            name='PersConcernee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, null=True)),
                ('sensible', models.BooleanField()),
                ('ordre', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Personne Concernée',
                'verbose_name_plural': 'Personnes Concernées',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Secteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name="Secteur d'Activité")),
                ('sensible', models.BooleanField(verbose_name='Est Sensible')),
                ('ordre', models.IntegerField(verbose_name="Ordre d'Affichage")),
            ],
        ),
        migrations.CreateModel(
            name='TypeClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name='Type de Client')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Description du Type de Client')),
                ('sensible', models.BooleanField(default=False, null=True, verbose_name='Est Sensible')),
                ('ordre', models.IntegerField(default=0, null=True, verbose_name="Ordre d'Affichage")),
            ],
            options={
                'verbose_name': 'Type Client',
                'verbose_name_plural': 'Types Clients',
            },
        ),
        migrations.CreateModel(
            name='TypePiece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name="Type de pièce d'identité")),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Description du Type de pièce')),
                ('sensible', models.BooleanField(default=False, null=True, verbose_name='Est Sensible')),
                ('ordre', models.IntegerField(default=0, null=True, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Type de pièce',
                'verbose_name_plural': 'Types de pièces',
            },
        ),
        migrations.CreateModel(
            name='SousFinalite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('sensible', models.BooleanField()),
                ('ordre', models.IntegerField()),
                ('finalite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_edcp.finalite')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date et heure de création')),
                ('is_read', models.BooleanField(default=False, verbose_name='Est lu')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='JournalTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField()),
                ('transaction', models.CharField(max_length=100)),
                ('cible', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Journal Transaction',
                'verbose_name_plural': 'Journals Transactions',
            },
        ),
        migrations.CreateModel(
            name='Habilitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField()),
                ('fonction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_edcp.fonction')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_edcp.role')),
            ],
        ),
        migrations.CreateModel(
            name='Enregistrement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')),
                ('raisonsociale', models.CharField(blank=True, max_length=100, verbose_name='Nom ou Raison Sociale')),
                ('representant', models.CharField(blank=True, max_length=100, verbose_name='Représentant légal')),
                ('rccm', models.CharField(blank=True, max_length=100, null=True, verbose_name='Numéro RCCM')),
                ('presentation', models.CharField(max_length=255, null=True, verbose_name="Présentation de l'activité")),
                ('telephone', models.CharField(max_length=20, null=True, verbose_name='Téléphone')),
                ('email_contact', models.CharField(max_length=100, null=True, verbose_name='Email de Contact')),
                ('site_web', models.CharField(blank=True, max_length=100, null=True, verbose_name='Site Web')),
                ('ville', models.CharField(max_length=100, null=True, verbose_name='Ville')),
                ('adresse_geo', models.CharField(max_length=100, null=True, verbose_name='Adresse Géographique')),
                ('adresse_bp', models.CharField(blank=True, max_length=100, null=True, verbose_name='Boîte Postale')),
                ('gmaps_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='Lien Google Maps')),
                ('effectif', models.IntegerField(blank=True, null=True, verbose_name='Effectif')),
                ('num_piece', models.CharField(blank=True, max_length=100, null=True, verbose_name='Numéro de la pièce')),
                ('has_dpo', models.BooleanField(default=False, verbose_name='A désigné un Correspondant')),
                ('pays', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_edcp.pays', verbose_name='Pays')),
                ('secteur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_edcp.secteur', verbose_name="Secteur d'Activité")),
                ('type_piece', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='base_edcp.typepiece', verbose_name="Type de pièce d'identité")),
                ('typeclient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base_edcp.typeclient', verbose_name='Type de Client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Enregistrement',
                'verbose_name_plural': 'Enregistrements',
            },
        ),
        migrations.CreateModel(
            name='Autorisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_autorisation', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('enregistrement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autorisations', to='base_edcp.enregistrement')),
            ],
        ),
    ]
