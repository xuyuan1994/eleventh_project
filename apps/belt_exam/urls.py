from django.conf.urls import url,include
from . import views

urlpatterns = [
   url('^$',views.index),
   url('^register$',views.register),
   url('^dashboard$',views.login),
   url('^logout$',views.logout),
   url('^wish_item/create$',views.create),
   url('^process$',views.process),
   url(r'^wish_item/(?P<item_id>\d+)', views.item),
   url(r'^delete/(?P<item_id>\d+)', views.delete),
   url(r'^remove/(?P<item_id>\d+)', views.remove),
   url(r'^add/(?P<item_id>\d+)', views.add),
   url('^Home$',views.back_to_home),
]