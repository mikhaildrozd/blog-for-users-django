from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog')
    title = models.CharField(max_length=50, verbose_name='Название блога')
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscriptions', blank=True,
                                         symmetrical=False)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'



    def __str__(self):
        return self.title


class Article(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts', verbose_name='Блог', db_index=True)
    title = models.CharField(max_length=130, db_index=True, verbose_name='Название статьи')
    content = models.TextField(blank=True, verbose_name='Текст статьи', )
    created = models.DateTimeField(auto_now=True, verbose_name='Создан')
    author = models.CharField(max_length=50, verbose_name='Автор блога')
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_articles', blank=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.author = self.blog.user.username
        return super(Article, self).save()


@receiver(post_save, sender=User)
def auto_create_blog(instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance)

