# Generated by Django 5.0.6 on 2024-05-18 21:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='blog.post', verbose_name='Пост комментария'),
        ),
    ]
