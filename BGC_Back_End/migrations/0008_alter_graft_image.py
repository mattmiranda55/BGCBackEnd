# Generated by Django 4.2.2 on 2023-12-23 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BGC_Back_End', '0007_alter_graft_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graft',
            name='image',
            field=models.CharField(null=True),
        ),
    ]
