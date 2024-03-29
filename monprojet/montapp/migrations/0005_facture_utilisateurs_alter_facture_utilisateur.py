# Generated by Django 5.0 on 2024-01-02 12:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('montapp', '0004_facture'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='utilisateurs',
            field=models.ManyToManyField(blank=True, related_name='factures_associees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='facture',
            name='utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factures', to=settings.AUTH_USER_MODEL),
        ),
    ]
