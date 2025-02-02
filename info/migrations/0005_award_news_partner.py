# Generated by Django 4.2.4 on 2024-02-09 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_headerimage_description_headerimage_description_ar_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Award Name')),
                ('name_en', models.CharField(max_length=250, null=True, verbose_name='Award Name')),
                ('name_ar', models.CharField(max_length=250, null=True, verbose_name='Award Name')),
                ('organization', models.CharField(max_length=250, verbose_name='Awarding Organization')),
                ('organization_en', models.CharField(max_length=250, null=True, verbose_name='Awarding Organization')),
                ('organization_ar', models.CharField(max_length=250, null=True, verbose_name='Awarding Organization')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_ar', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('date', models.DateField(verbose_name='Date')),
                ('image', models.ImageField(upload_to='home/awards', verbose_name='Image')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
            ],
            options={
                'verbose_name': 'Award',
                'verbose_name_plural': 'Awards',
                'ordering': ('-create_at', '-update_at'),
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('title_en', models.CharField(max_length=250, null=True, verbose_name='Title')),
                ('title_ar', models.CharField(max_length=250, null=True, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('description_en', models.TextField(null=True, verbose_name='Description')),
                ('description_ar', models.TextField(null=True, verbose_name='Description')),
                ('date', models.DateField(verbose_name='Publication Date')),
                ('alt', models.CharField(help_text='Text is meant to convey the “why” of the image as it relates to the content of a document or webpage', max_length=250, verbose_name='Alternative (Alt)')),
                ('alt_en', models.CharField(help_text='Text is meant to convey the “why” of the image as it relates to the content of a document or webpage', max_length=250, null=True, verbose_name='Alternative (Alt)')),
                ('alt_ar', models.CharField(help_text='Text is meant to convey the “why” of the image as it relates to the content of a document or webpage', max_length=250, null=True, verbose_name='Alternative (Alt)')),
                ('image', models.ImageField(upload_to='home/news', verbose_name='Image')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
                'ordering': ('-create_at', '-update_at'),
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Partner Name')),
                ('name_en', models.CharField(max_length=250, null=True, verbose_name='Partner Name')),
                ('name_ar', models.CharField(max_length=250, null=True, verbose_name='Partner Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_ar', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('image', models.ImageField(upload_to='home/partners', verbose_name='Image')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
            ],
            options={
                'verbose_name': 'Partner',
                'verbose_name_plural': 'Partners',
                'ordering': ('-create_at', '-update_at'),
            },
        ),
    ]
