# Generated by Django 5.1.2 on 2024-12-12 21:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('specialties', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimated_cost', models.IntegerField()),
                ('estimated_duration', models.IntegerField()),
                ('location', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotations', to='users.technician')),
            ],
        ),
        migrations.CreateModel(
            name='QuotationService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_services', to='requests.quotation')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_services', to='services.service')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('customer_comment', models.TextField()),
                ('technician_comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id_specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specialties.specialty')),
                ('rut_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='requests.requeststatus')),
            ],
        ),
        migrations.AddField(
            model_name='quotation',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotations', to='requests.request'),
        ),
    ]
