# Generated by Django 4.2.2 on 2023-08-14 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BGC_Back_End', '0013_alter_graft_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graft',
            name='documents',
            field=models.TextField(blank=True, null=True),
        ),
    ]
