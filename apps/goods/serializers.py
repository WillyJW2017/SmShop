from rest_framework import serializers
from django.db.models import Q

from goods.models import Goods, GoodsCategory, HotSearchWords, GoodsImage, Banner, GoodsCategoryBrand, IndexAd

# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100, required=True)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()

class GoodsCategorySerializer3(serializers.ModelSerializer):
    '''
    商品类别序列化
    '''
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsCategorySerializer2(serializers.ModelSerializer):
    '''
    商品类别序列化
    '''
    sub_cat = GoodsCategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsCategorySerializer(serializers.ModelSerializer):
    '''
    商品类别序列化
    '''
    sub_cat = GoodsCategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image', )

class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    # images 名字与 GoodsImage models 的外键(goods) related_name='images' 一致
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'

class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = ('keywords',)

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'

class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True) #一个category对应多个brand，使用many=True
    goods = serializers.SerializerMethodField()
    sub_cat = GoodsCategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_instance = ad_goods[0].goods
            goods_json = GoodsSerializer(good_instance, many=False, context={'request' : self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request' : self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'