# Generated by Django 4.0.5 on 2022-07-15 15:21

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homescr', '0004_solutions_uname'),
    ]

    operations = [
        migrations.AddField(
            model_name='problems',
            name='in_formate',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='problems',
            name='out_formate',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='problems',
            name='problem_st',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
