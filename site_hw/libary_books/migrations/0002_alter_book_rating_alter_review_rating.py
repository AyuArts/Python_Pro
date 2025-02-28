# Generated by Django 5.1.4 on 2025-01-10 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libary_books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.FloatField(db_index=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(db_index=True, default=0),
        ),
    ]
