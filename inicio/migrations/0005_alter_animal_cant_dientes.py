# Generated by Django 4.1.7 on 2023-04-25 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0004_alter_animal_cant_dientes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='cant_dientes',
            field=models.IntegerField(null=True),
        ),
    ]