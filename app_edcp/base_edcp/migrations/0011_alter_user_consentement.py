# Generated by Django 4.2.14 on 2024-08-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_edcp', '0010_alter_user_avatar_alter_user_consentement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='consentement',
            field=models.BooleanField(help_text="Veuillez cocher cette case pour donner votre consentement : \n        les données soumises via ce formulaire seront utilisées pour la création \n        et pour l'accomplissement de vos formalités sur la plateforme e-DCP. \n        Vos données ne seront traitées que par les agents habilités de l'Autorité de Protection.\n        Vous pouvez à tous moments exercer vos droits exercer à l'adresse ..... ", null=True, verbose_name='Recueil du consentement'),
        ),
    ]