# Generated by Django 2.0 on 2018-01-20 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20180115_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('token', models.CharField(max_length=30, null=True)),
                ('expires', models.DateTimeField(null=True)),
            ],
        ),
    ]
