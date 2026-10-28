import random

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from characters.models import Character
from characters.serializers import CharacterSerializer


@api_view(["GET"])
def get_random_characters_view(request: Request) -> Response:
    pks = Character.objects.values_list("pk", flat=True)
    random_pk = random.choice(pks)
    random_obj = Character.objects.get(pk=random_pk)
    serializer = CharacterSerializer(random_obj)
    return Response(serializer.data, status=status.HTTP_200_OK)

