# Generated by Django 5.1.3 on 2024-12-09 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nancy', '0004_alter_moviequery_recommended_movies'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('actors', models.CharField(blank=True, max_length=500)),
                ('directors', models.CharField(blank=True, max_length=500)),
                ('release_year', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('genres', models.ManyToManyField(to='nancy.genre')),
            ],
        ),
    ]
