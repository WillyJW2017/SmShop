from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from .serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    用户收藏功能
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 重载get_queryset方法
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)