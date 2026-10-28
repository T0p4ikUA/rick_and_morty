from django.urls import path

from characters.views import get_random_characters

app_name = "characters"

urlpatterns = [
    path("characters/random/", get_random_characters, name="characters_random"),
]