# Generated by Django 3.2.7 on 2021-10-01 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0005_alter_column_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='order',
            field=models.IntegerField(),
        ),
    ]
