import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision"
    "/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832"
    "&fill=transparent"
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = PokemonEntity.objects.all()
    for pokemon_entity in pokemons:
        try:
            image = request.build_absolute_uri(
                pokemon_entity.pokemon.photo.url
            )
        except ValueError:
            image = ""
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon, image)

    pokemons_on_page = []
    types_of_pokemons = Pokemon.objects.all()
    for pokemon in types_of_pokemons:
        try:
            image = request.build_absolute_uri(pokemon.photo.url)
        except ValueError:
            image = ""
        pokemons_on_page.append(
            {
                "pokemon_id": pokemon.pk,
                "img_url": image,
                "title_ru": pokemon.title,
            }
        )

    return render(
        request,
        "mainpage.html",
        context={
            "map": folium_map._repr_html_(),
            "pokemons": pokemons_on_page,
        },
    )


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    requested_pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    pokemons_entities = requested_pokemon.pokemon_type.all()
    next_evolution = requested_pokemon.pokemon_evolutions.last()

    try:
        requested_pokemon_image = request.build_absolute_uri(
            requested_pokemon.photo.url
        )
    except ValueError:
        requested_pokemon_image = ""

    try:
        previous_evolution_image = request.build_absolute_uri(
            requested_pokemon.previous_evolution.photo.url
        )
    except ValueError:
        previous_evolution_image = ""

    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            requested_pokemon_image,
        )

    about_pokemon = {
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "img_url": requested_pokemon_image,
        "description": requested_pokemon.description,
        "previous_evolution": {
            "title_ru": requested_pokemon.previous_evolution.title,
            "pokemon_id": requested_pokemon.previous_evolution.pk,
            "img_url": previous_evolution_image,
        },
    }
    if next_evolution:
        next_evolution_image = request.build_absolute_uri(
            next_evolution.photo.url
        )
        about_pokemon["next_evolution"] = {
            "title_ru": next_evolution.title,
            "pokemon_id": next_evolution.pk,
            "img_url": next_evolution_image,
        }

    return render(
        request,
        "pokemon.html",
        context={"map": folium_map._repr_html_(), "pokemon": about_pokemon},
    )
