# Generated by Django 4.2.1 on 2023-06-02 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='aggression',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='original_content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
