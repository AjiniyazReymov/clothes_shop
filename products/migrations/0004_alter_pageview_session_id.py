# Generated by Django 5.1.4 on 2024-12-08 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_pageview_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageview',
            name='session_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
