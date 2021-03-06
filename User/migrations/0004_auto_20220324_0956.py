# Generated by Django 3.2 on 2022-03-24 07:56

import HelperClasses.DjangoValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20220324_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=14, unique=True, validators=[HelperClasses.DjangoValidator.DjangoValidator.validation_EgyptionMobileNumber]),
        ),
        migrations.AlterField(
            model_name='user',
            name='number_of_identification',
            field=models.CharField(db_column='number_of_identification', max_length=14, unique=True, validators=[HelperClasses.DjangoValidator.DjangoValidator.validation_numberOfIdentintification]),
        ),
    ]
