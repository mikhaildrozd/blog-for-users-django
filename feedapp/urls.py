from django.urls import path
from . import views

app_name = 'feedapp'

urlpatterns = [
    path('', views.MyFeed.as_view(), name='subscribers'),
    path('subscriptions/', views.SubscribersListView.as_view(), name='edit_subscribers'),
    path('update_sub/<int:pk>/', views.EditSubscribersView.as_view(), name='edit'),
    path('update_art/update/<int:pk>/', views.EditReadBy.as_view(), name='read_by'),
]