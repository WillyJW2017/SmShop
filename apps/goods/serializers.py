from rest_framework import serializers

from goods.models import Goods, GoodsCategory, HotSearchWords, GoodsImage

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
