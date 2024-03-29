# Generated by Django 4.2.2 on 2023-12-16 21:27

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('BGC_Back_End', '0005_alter_graft_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graft',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='graft',
            name='image',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(), upload_to='grafts/images/'),
        ),
    ]
