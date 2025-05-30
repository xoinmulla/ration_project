# Generated by Django 5.1.7 on 2025-05-09 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('beneficiary_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RationItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('unit', models.CharField(max_length=20)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='DistributionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_distribution', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('ration_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beneficiary_management.rationcard')),
            ],
        ),
        migrations.CreateModel(
            name='DistributionItemDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_distributed', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_at_distribution', models.DecimalField(decimal_places=2, max_digits=10)),
                ('distribution_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_distributed', to='distribution_management.distributionrecord')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribution_management.rationitem')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribution_management.rationitem')),
            ],
        ),
    ]
