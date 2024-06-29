# Generated by Django 4.1.7 on 2023-04-21 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0006_remove_generalreviews_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalreviews',
            name='img',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userreviews',
            name='img',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userreviews',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]