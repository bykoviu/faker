# Generated by Django 3.2.7 on 2021-09-30 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0002_alter_schema_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('order', models.IntegerField(unique=True)),
                ('type', models.CharField(max_length=50)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schemas.schema')),
            ],
            options={
                'verbose_name': 'column',
                'verbose_name_plural': 'columns',
                'ordering': ('title',),
            },
        ),
    ]
