from django.contrib import admin
from .models import Blog, Article
from django import forms
from django.core.exceptions import ValidationError


class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('slug',)

    def clean(self):
        if self.cleaned_data.get('user') in self.cleaned_data.get('subscribers'):
            raise ValidationError(" Невозможно себя добавить в подписчики")
        return super(BlogAdminForm, self).clean()


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('user', 'title',)


@admin.register(Article)
class BlogArticleAdmin(admin.ModelAdmin):
    exclude = ('author',)

    list_display = ('title', 'blog', 'author', 'created')

  
