# Generated by Django 4.2.1 on 2023-06-05 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_rename_now_step_now_step_me_now_step_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Me_Now_step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('me_now_step', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Other_Now_step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_now_step', models.TextField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Now_step',
        ),
    ]
