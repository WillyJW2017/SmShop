from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
import json
from goods.models import Goods
from django.forms.models import model_to_dict
from django.core import serializers


class GoodsListView(View):
    def get(self, request):
        '''
        通过django的view实现商品列表页
        :param request:
        :return:
        '''
        json_list = []
        goods = Goods.objects.all()[:10]

        # 使用此方法比较繁琐，需要逐个添加字段
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)
        # return HttpResponse(json.dumps(json_list), content_type='application/json')

        # 使用model_to_dict后有一些字段不能序列化：ImageFieldFile，
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        # return HttpResponse(json.dumps(json_list), content_type='application/json')

        # 使用serializers非常简洁
        json_data = serializers.serialize('json',goods)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)
