from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('myblog/update-article/<int:pk>/', views.ArticleUpdateView.as_view(), name='updates'),
    path('myblog/<int:pk>/', views.AuthorArticleList.as_view(), name='my_blog'),
    path('bloglist/', views.BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', views.ReadArticle.as_view(), name='article_detail'),
    path('myblog/article/<int:pk>/', views.ReadMyArticle.as_view(), name='my_article'),
    path('create-article/', views.ArticleCreateView.as_view(), name='article_create'),
    path('myarticle/delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='article_delete'),

]