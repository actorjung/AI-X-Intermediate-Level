# Generated by Django 4.2.1 on 2023-06-05 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment_aggression_comment_original_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Now_step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('now_step', models.TextField(null=True)),
            ],
        ),
    ]
