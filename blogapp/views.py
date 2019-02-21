from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Blog, Article
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class BlogListView(LoginRequiredMixin, ListView):
    template_name = 'blogapp/bloglist.html'
    queryset = Blog.objects.order_by('user__username')


class AuthorArticleList(LoginRequiredMixin, ListView):
    template_name = 'blogapp/articlelist.html'

    def get_queryset(self):
        self.blog = get_object_or_404(Blog, pk=self.kwargs['pk'], user=self.request.user)
        return self.blog.posts.order_by('-created')


class ReadArticle(LoginRequiredMixin, DetailView):
    template_name = 'blogapp/read_article.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Article, pk=self.kwargs['pk'], blog__in=self.request.user.subscriptions.all())


class ReadMyArticle(LoginRequiredMixin, DetailView):
    template_name = 'blogapp/read_article.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Article, pk=self.kwargs['pk'], author=self.request.user)


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'blogapp/create_article.html'
    fields = ('title', 'content',)

    def form_valid(self, form):
        new_article = form.save(commit=False)
        new_article.blog = self.request.user.blog
        new_article.save()
        return redirect(reverse_lazy('blog:my_blog', args=[self.request.user.blog.pk]))


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blogapp/create_article.html'
    fields = ('title', 'content',)

    def get_success_url(self):
        return reverse_lazy('blog:my_blog', args=[self.request.user.blog.pk])

    def get_object(self, queryset=None):
        return get_object_or_404(Article, pk=self.kwargs['pk'], author=self.request.user)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = 'article'

    def get_success_url(self):
        return reverse_lazy('blog:my_blog', args=[self.request.user.blog.pk])

    def get_object(self, queryset=None):
        return get_object_or_404(Article, pk=self.kwargs['pk'], author=self.request.user)
