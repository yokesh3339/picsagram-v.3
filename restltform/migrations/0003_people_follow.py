# Generated by Django 3.1.1 on 2020-11-16 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restltform', '0002_auto_20201115_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='follow',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='restltform.follow'),
            preserve_default=False,
        ),
    ]
