# Generated by Django 5.2 on 2025-05-08 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_score_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='pass_rate',
            field=models.FloatField(default=0.75),
        ),
    ]
