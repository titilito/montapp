# Generated by Django 5.0 on 2023-12-31 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('montapp', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('Compte rendu', 'Compte rendu'), ('Règlement', 'Règlement'), ('Avenant', 'Avenant'), ('Autre', 'Autre')], max_length=255),
        ),
    ]
