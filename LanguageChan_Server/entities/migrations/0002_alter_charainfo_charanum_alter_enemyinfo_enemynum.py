# Generated by Django 5.1.1 on 2024-09-23 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charainfo',
            name='charanum',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='enemyinfo',
            name='enemynum',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
