# Generated by Django 4.2.2 on 2023-06-27 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BGC_Back_End', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='business_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='num_credits',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
