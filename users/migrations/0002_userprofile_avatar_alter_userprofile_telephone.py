# Generated by Django 4.1.2 on 2022-10-16 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='default_avatar.jpg', null=True, upload_to='avatar'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='telephone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Telephone number'),
        ),
    ]
