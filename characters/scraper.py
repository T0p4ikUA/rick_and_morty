import time
import requests
from django.conf import settings
from characters.models import Character


def scrape_characters() -> list[Character]:
    next_url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL
    characters = []

    while next_url_to_scrape is not None:
        response = requests.get(next_url_to_scrape)
        characters_response = response.json()

        for character_dict in characters_response["results"]:
            characters.append(
                Character(
                    api_id=character_dict["id"],
                    name=character_dict["name"],
                    status=character_dict["status"],
                    species=character_dict["species"],
                    gender=character_dict["gender"],
                    image=character_dict["image"],
                )
            )

        next_url_to_scrape = characters_response["info"]["next"]
        time.sleep(0.2)

    return characters


def save_characters(characters: list[Character]) -> None:
    for character in characters:
        Character.objects.update_or_create(
            api_id=character.api_id,
            defaults={
                "name": character.name,
                "status": character.status,
                "species": character.species,
                "gender": character.gender,
                "image": character.image,
            },
        )


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
