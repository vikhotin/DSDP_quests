# Generated by Django 2.0 on 2018-01-09 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20180109_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='quests_completed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='quests_number',
            field=models.IntegerField(default=0),
        ),
    ]