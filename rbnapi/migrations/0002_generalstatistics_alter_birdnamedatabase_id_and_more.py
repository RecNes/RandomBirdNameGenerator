# Generated by Django 4.0.6 on 2022-07-15 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbnapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_count', models.BigIntegerField(default=0, verbose_name='Count Number')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Last Update')),
            ],
            options={
                'ordering': ['updated'],
            },
        ),
        migrations.AlterField(
            model_name='birdnamedatabase',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='birdnamedatabase',
            name='scientific_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bird_name', to='rbnapi.scientificname'),
        ),
        migrations.AlterField(
            model_name='scientificname',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='RequestRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_ip', models.GenericIPAddressField(verbose_name='Client IP')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Request Date')),
                ('statistic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_record', to='rbnapi.generalstatistics')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.AddField(
            model_name='generalstatistics',
            name='bird_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistic', to='rbnapi.birdnamedatabase'),
        ),
    ]
