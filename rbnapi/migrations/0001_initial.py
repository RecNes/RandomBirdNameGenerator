# coding: utf-8
from __future__ import unicode_literals


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BirdNameDatabase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bird_name', models.TextField(unique=True, verbose_name='Bird Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScientificName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scientific_name', models.TextField(unique=True, verbose_name='Scientific Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='birdnamedatabase',
            name='scientific_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbnapi.ScientificName'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='birdnamedatabase',
            unique_together=set([('bird_name', 'scientific_name')]),
        ),
    ]
