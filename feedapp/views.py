from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from blogapp.models import Blog, Article
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


class MyFeed(ListView):
    template_name = 'feedapp/myfeed.html'

    def get_queryset(self):
        return Article.objects.filter(blog__in=self.request.user.subscriptions.all()).order_by('-created')


class SubscribersListView(LoginRequiredMixin, ListView):
    template_name = 'feedapp/subscriberslist.html'

    def get_queryset(self):
        return self.request.user.subscriptions.order_by('user__username')


class EditSubscribersView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        if self.blog.user != request.user:
            if request.user not in self.blog.subscribers.all():

                self.blog.subscribers.add(request.user)
            else:
                self.blog.subscribers.remove(request.user)
                self.delete_read_by(request.user, self.blog)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def delete_read_by(self, user, blog):
        articles = blog.posts.all()
        for article in articles:
            article.read_by.remove(user)


class EditReadBy(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        if request.user not in article.read_by.all():
            article.read_by.add(request.user)
        else:
            article.read_by.remove(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
