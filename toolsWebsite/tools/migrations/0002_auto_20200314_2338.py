# Generated by Django 2.2.6 on 2020-03-14 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolcategory',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
