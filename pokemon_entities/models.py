from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField("Название", max_length=200)
    title_en = models.CharField("Англ. название", max_length=200, blank=True)
    title_jp = models.CharField("Яп. название", max_length=200, blank=True)
    description = models.TextField("Описание", blank=True)
    photo = models.ImageField("Изображение", null=True, blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        verbose_name="Из кого эволюционирует",
        null=True,
        blank=True,
        default=None,
        related_name="pokemon_evolutions",
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name="Название",
        on_delete=models.CASCADE,
        related_name="pokemon_type"
    )
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    appeared_at = models.DateTimeField(
        "Время появления", null=True, blank=True
    )
    disappeared_at = models.DateTimeField(
        "Время исчезновения", null=True, blank=True
    )
    level = models.IntegerField("Уровень")
    health = models.IntegerField("Здоровье", null=True, blank=True)
    strength = models.IntegerField("Сила", null=True, blank=True)
    defence = models.IntegerField("Защита", null=True, blank=True)
    stamina = models.IntegerField("Выносливость", null=True, blank=True)

    def __str__(self):
        return f"{self.pokemon} lvl: {self.level}"
