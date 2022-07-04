from rest_framework.generics import GenericAPIView

from user.models import User
from user.serializers import UserSerializer
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin, DestroyModelMixin


class UserMixin(GenericAPIView, ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin):

    """
    Used mixins for CRUD operations
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def delete(self, request, pk):
        try:
            return self.destroy(request, pk)
        except Exception as e:
            print(e)


class UserCreate(GenericAPIView, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk):
        return self.retrieve(request)
