# Generated by Django 4.2.2 on 2023-08-01 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BGC_Back_End', '0006_remove_profile_username_graft_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graft',
            name='created_by',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='graft',
            name='image',
            field=models.ImageField(null=True, upload_to='grafts/images/'),
        ),
    ]
