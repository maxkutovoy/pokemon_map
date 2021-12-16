# Generated by Django 3.1.14 on 2021-12-16 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('title_en', models.CharField(blank=True, default='', max_length=200, verbose_name='Англ. название')),
                ('title_jp', models.CharField(blank=True, default='', max_length=200, verbose_name='Яп. название')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('previous_evolution', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pokemon_evolutions', to='pokemon_entities.pokemon', verbose_name='Из кого эволюционирует')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(verbose_name='Широта')),
                ('lon', models.FloatField(verbose_name='Долгота')),
                ('appeared_at', models.DateTimeField(blank=True, null=True, verbose_name='Время появления')),
                ('disappeared_at', models.DateTimeField(blank=True, null=True, verbose_name='Время исчезновения')),
                ('level', models.IntegerField(verbose_name='Уровень')),
                ('health', models.IntegerField(blank=True, null=True, verbose_name='Здоровье')),
                ('strength', models.IntegerField(blank=True, null=True, verbose_name='Сила')),
                ('defence', models.IntegerField(blank=True, null=True, verbose_name='Защита')),
                ('stamina', models.IntegerField(blank=True, null=True, verbose_name='Выносливость')),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_type', to='pokemon_entities.pokemon', verbose_name='Название')),
            ],
        ),
    ]
