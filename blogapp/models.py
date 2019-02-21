from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from django.conf import settings
from django.template.defaultfilters import slugify
from unidecode import unidecode


class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog')
    title = models.CharField(max_length=50, verbose_name='Название блога')
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscriptions', blank=True,
                                         symmetrical=False)
    slug = models.SlugField(max_length=80, unique=True, )

    class Meta():
        pass

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(unidecode(self.user.username))
        return super(Blog, self).save()

    def get_absolute_url(self):
        return reverse('blogapp:blog',
                       args=[self.slug])



class Article(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts', verbose_name='Блог', db_index=True)
    title = models.CharField(max_length=130, db_index=True, verbose_name='Название статьи')
    content = models.TextField(blank=True, verbose_name='Текст статьи', )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    author = models.CharField(max_length=50, verbose_name='Автор блога')

    class Meta():
        pass

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.author = self.blog.user.username
        return super(Article, self).save()

    def get_absolute_url(self):
        return reverse('blogapp:article',
                       args=[self.pk])

