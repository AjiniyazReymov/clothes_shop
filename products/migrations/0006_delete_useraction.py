# Generated by Django 5.1.4 on 2024-12-08 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_useraction_options_remove_useraction_action_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserAction',
        ),
    ]
