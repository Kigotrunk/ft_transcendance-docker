# Generated by Django 5.0.4 on 2024-06-26 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_alter_partie_player1_alter_partie_player2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partie',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
