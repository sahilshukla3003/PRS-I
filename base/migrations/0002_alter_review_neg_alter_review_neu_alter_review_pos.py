# Generated by Django 4.1.7 on 2023-04-09 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='neg',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='neu',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='pos',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
