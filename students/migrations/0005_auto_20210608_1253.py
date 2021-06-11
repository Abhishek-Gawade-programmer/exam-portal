# Generated by Django 3.2.4 on 2021-06-08 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20210608_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='teacher',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reportquestion',
            name='student',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentanswer',
            name='student',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='test',
            name='teacher',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userquestionlist',
            name='student',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]