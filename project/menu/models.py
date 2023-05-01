from django.db import models


# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Заголовок меню')
    slug = models.SlugField(max_length=255, verbose_name="Slug меню ")

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class Submenu(models.Model):
    name = models.CharField(max_length=255, verbose_name='Заголовок подменю')
    slug = models.SlugField(max_length=255, verbose_name="Slug подменю")
    menu = models.ForeignKey(Menu, blank=True, related_name='items', on_delete=models.CASCADE)
    parent_submenu = models.ForeignKey('self', blank=True, null=True, related_name='submenus', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подменю'
        verbose_name_plural = 'Подменю'

    def __str__(self):
        return self.name
