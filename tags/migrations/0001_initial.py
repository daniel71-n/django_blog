# Generated by Django 3.0 on 2020-07-18 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('tag_name', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
    ]
