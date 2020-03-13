# Generated by Django 3.0.2 on 2020-03-13 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToolCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
                ('available', models.IntegerField(default=0)),
                ('unavailable', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('tool_image', models.ImageField(default='', upload_to=None)),
            ],
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
