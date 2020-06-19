# Generated by Django 3.0.6 on 2020-06-02 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classes',
            name='run_date_time',
        ),
        migrations.AddField(
            model_name='classes',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='classes',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]