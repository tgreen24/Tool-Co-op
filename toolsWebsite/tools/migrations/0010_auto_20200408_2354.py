# Generated by Django 2.2 on 2020-04-09 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0009_auto_20200408_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date_returned',
            field=models.DateTimeField(null=True),
        ),
    ]
