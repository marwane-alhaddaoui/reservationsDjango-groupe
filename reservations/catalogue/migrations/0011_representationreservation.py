# Generated by Django 5.1.2 on 2025-01-13 23:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0010_artistetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepresentationReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='representation_reservations', to='catalogue.price')),
                ('representation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='representation_reservations', to='catalogue.representation')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='representation_reservations', to='catalogue.reservation')),
            ],
            options={
                'db_table': 'representation_reservation',
            },
        ),
    ]
