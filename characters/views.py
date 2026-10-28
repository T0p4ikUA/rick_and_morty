import random

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from characters.models import Character
from characters.serializers import CharacterSerializer


@extend_schema(
    responses={status.HTTP_200_OK: CharacterSerializer}
)
@api_view(["GET"])
def get_random_characters_view(request: Request) -> Response:
    """ Get random characters  from Rick and Morty World"""
    pks = Character.objects.values_list("pk", flat=True)
    random_pk = random.choice(pks)
    random_obj = Character.objects.get(pk=random_pk)
    serializer = CharacterSerializer(random_obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterListView(ListAPIView):
    serializer_class = CharacterSerializer

    def get_queryset(self):
        queryset = Character.objects.all()

        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="name by insensitive contains",
                required=False,
                type=str
            )
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:
        """ List Character with filter by name"""
        return super().get(request, *args, **kwargs)
