# urls.py
from django.urls import path
from .views import HomeView,ItemList,StorageLocationList,CategoryList,ItemCreate,StorageLocationCreate,CategoryCreate,ItemUpdate,StorageLocationUpdate,CategoryUpdate,ItemDelete,StorageLocationDelete,CategoryDelete
from django.views.generic.base import TemplateView

app_name ='ahinventory'

urlpatterns = [
#    path('', TemplateView.as_view(template_name='ahinventoryhome.html'),name='search'),
    path('',HomeView.as_view(),name='home'),
    path('items/', ItemList.as_view(),name='item-list'),
    path('items/add/', ItemCreate.as_view(), name='item-add'),
    path('items/<int:pk>/', ItemUpdate.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', ItemDelete.as_view(), name='item-delete'),
    path('storagelocations/', StorageLocationList.as_view(),name='storagelocation-list'),
    path('storagelocations/add/', StorageLocationCreate.as_view(), name='storagelocation-add'),
    path('storagelocations/<int:pk>/', StorageLocationUpdate.as_view(), name='storagelocation-update'),
    path('storagelocations/<int:pk>/delete/', StorageLocationDelete.as_view(), name='storagelocation-delete'),
    path('categories/', CategoryList.as_view(),name='category-list'),
    path('categories/add/', CategoryCreate.as_view(), name='category-add'),
    path('categories/<int:pk>/', CategoryUpdate.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDelete.as_view(), name='category-delete'),
#    path('search/',search,name='search'),
#    path('storeitem/',store_item,name='store-item'),
]
