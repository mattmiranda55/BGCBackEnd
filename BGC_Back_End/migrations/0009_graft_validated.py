# Generated by Django 4.2.2 on 2023-08-01 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BGC_Back_End', '0008_graft_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='graft',
            name='validated',
            field=models.BooleanField(default=False),
        ),
    ]
