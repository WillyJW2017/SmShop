import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(filters.FilterSet):
    '''
    商品的过滤类
    '''
    pricemin = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')
    pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    # name = django_filters.CharFilter(name='name', lookup_expr='icontains') # 模糊查询，不区分大小写
    top_category = django_filters.NumberFilter(method='top_category_filter')
    # 返回一级目录下所有的二级和三级目录
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    # 实现价格区间的功能
    class Meta:
        model = Goods
        fields = ['pricemin','pricemax', 'is_hot']
