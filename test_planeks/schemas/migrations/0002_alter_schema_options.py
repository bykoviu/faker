# Generated by Django 3.2.7 on 2021-09-24 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schema',
            options={'ordering': ('updated',), 'verbose_name': 'schema', 'verbose_name_plural': 'schemas'},
        ),
    ]
