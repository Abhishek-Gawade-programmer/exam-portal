# Generated by Django 3.2.4 on 2021-06-08 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20210608_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportquestion',
            name='student',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.student'),
        ),
        migrations.AlterField(
            model_name='studentanswer',
            name='student',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.student'),
        ),
        migrations.AlterField(
            model_name='userquestionlist',
            name='student',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.student'),
        ),
    ]
