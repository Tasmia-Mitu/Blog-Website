# Generated by Django 4.2.4 on 2023-09-05 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_delete_blogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profile_pics/profile'),
        ),
    ]
