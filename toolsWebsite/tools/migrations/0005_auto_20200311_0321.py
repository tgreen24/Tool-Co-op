# Generated by Django 2.2.6 on 2020-03-11 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_toolcategory_duedates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolcategory',
            name='dueDates',
        ),
        migrations.CreateModel(
            name='DueDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.CharField(max_length=200)),
                ('date_bought', models.DateTimeField()),
                ('date_due', models.DateTimeField()),
                ('toolCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.ToolCategory')),
            ],
        ),
    ]
