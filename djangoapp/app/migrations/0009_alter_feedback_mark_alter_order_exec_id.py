# Generated by Django 5.0.3 on 2024-04-19 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_feedback_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='mark',
            field=models.CharField(choices=[('1.0', '1.0'), ('1.5', '1.5'), ('2.0', '2.0'), ('2.5', '2.5'), ('3.0', '3.0'), ('3.5', '3.5'), ('4.0', '4.0'), ('4.5', '4.5'), ('5.0', '5.0')], default='0.0', max_length=3),
        ),
        migrations.AlterField(
            model_name='order',
            name='exec_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.executor'),
        ),
    ]
