# Generated by Django 3.2.8 on 2021-10-20 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0007_alter_column_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='delimiter',
            field=models.CharField(default=',', max_length=50),
        ),
    ]