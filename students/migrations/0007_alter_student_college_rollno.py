# Generated by Django 3.2.4 on 2021-06-20 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20210620_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='college_rollno',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
