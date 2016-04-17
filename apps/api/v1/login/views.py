from rest_framework import response, viewsets
from rest_framework.decorators import list_route

from .serializers import FacebookLoginSerializer, LoginSerializer


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return response.Response({'token': token.key})

    @list_route(methods=['POST'], serializer_class=FacebookLoginSerializer)
    def facebook(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return response.Response({'token': token.key})
