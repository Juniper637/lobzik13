# Generated by Django 5.1.6 on 2025-03-06 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobzikapp', '0003_alter_star_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='star',
            options={'ordering': ['-time_create'], 'verbose_name': 'Знаменитость', 'verbose_name_plural': 'Знаменитости'},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, verbose_name='URL'),
        ),
        migrations.AddIndex(
            model_name='star',
            index=models.Index(fields=['-time_create'], name='lobzikapp_s_time_cr_3f1f3f_idx'),
        ),
    ]
