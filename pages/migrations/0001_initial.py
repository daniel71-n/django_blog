# Generated by Django 3.0 on 2020-07-31 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_name', models.CharField(max_length=50)),
                ('sender_email', models.EmailField(help_text='The email address of the individual who made contact', max_length=254)),
                ('additional_contact_information', models.TextField(blank=True)),
                ('about', models.CharField(help_text='A summary of what the inquiry is about', max_length=150)),
                ('inquiry_details', models.TextField(blank=True, help_text='A more detailed description of the inquiry')),
                ('submission_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
