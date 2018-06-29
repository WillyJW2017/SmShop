from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Goods, GoodsCategory, HotSearchWords
from .serializers import GoodsSerializer, GoodsCategorySerializer, HotWordsSerializer
from .filters import GoodsFilter

# Create your views here.


# class GoodsListView(APIView):
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)

# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     '''
#     商品列表页
#     '''
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

# 自定义分页功能，前端页面可以自己配置page_size参数： http://127.0.0.1:8000/goods/?p=2&page_size=20
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

# class GoodsListView(generics.ListAPIView):
#     '''
#     商品列表页
#     '''
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination  # 分页功能


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    商品列表页, 实现了分页、搜索、过滤、排序
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination  # 分页功能

    # 使用django_filters实现过滤功能
    # filter_backends = (DjangoFilterBackend,)
    # filter_class = GoodsFilter

    # 使用 drf 的filters 实现搜索
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter # 过滤
    search_fields = ('name', 'goods_brief', 'goods_desc') # 搜索
    ordering_fields = ('sold_num', 'shop_price')  # 排序

    # 自定义过滤功能
    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get('price_min', 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset



class GoodsCategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class HotWordsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HotSearchWords.objects.all()
    serializer_class = HotWordsSerializer