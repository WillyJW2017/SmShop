"""SmShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
import xadmin
from SmShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

# from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet, GoodsCategoryViewSet, HotWordsViewSet, BannerViewSet, IndexCategoryViewSet
from user_operation.views import UserFavViewSet

router = DefaultRouter()

# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 配置category的url
router.register(r'categorys', GoodsCategoryViewSet, base_name='categorys')

router.register(r'hotsearchs', HotWordsViewSet, base_name='hotsearchs')

# 配置用户收藏
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')

# 轮播图url
router.register(r'banners', BannerViewSet, base_name='banners')

#首页商品系列数据
router.register(r'indexgoods', IndexCategoryViewSet, base_name='indexgoods')

# 可以自己将get方法绑定到list
# goods_list = GoodsListViewSet.as_view({
#     'get':'list',
# })

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'docs/', include_docs_urls(title='我的平台')), # drf文档入口
    url(r'^api-auth/', include('rest_framework.urls')), # drf登录的配置
    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),
    # 商品列表页
    # url(r'^goods/$', GoodsListView.as_view(), name='goods-list')
    url(r'^', include(router.urls))
]
