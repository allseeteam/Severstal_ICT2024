from django.db import models


class Account(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='accounts',
        verbose_name='Пользователь',
        null=True
    )
    request = models.TextField(
        'Текст запроса пользователя',
        max_length=400 #Максимальная длина запроса к поисковику.
    )
    completed = models.BooleanField(
        'Готов',
        default=False
    )

    class Meta:
        verbose_name = 'Аналитический отчет'
        verbose_name_plural = 'Аналитические отчеты'


class WebPage(models.Model):
    url = models.CharField(
        'URL',
        max_length=1024
    )
    content = models.TextField(
        'Содержание страницы',
        blank=True
    )
    update_date = models.DateTimeField(
        'Дата обновления',
        null=True
    )
    accounts = models.ManyToManyField(
        'Account',
        related_name='pages'
    )
    user_add = models.BooleanField(
        'Добавлено пользователем',
        default=False
    )

    class Meta:
        verbose_name = 'Интернет страница'
        verbose_name_plural = 'Интернет страницы'


class WebVideo(models.Model):
    url = models.CharField(
        'URL',
        max_length=1024
    )
    content = models.TextField(
        'Содержание видео'
    )
    accounts = models.ManyToManyField(
        'Account',
        related_name='videos'
    )

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


class UserFiles(models.Model):
    name = models.CharField(
        'Название файла'
    )
    file = models.FileField(
        upload_to='files/'
    )

    class Meta:
        verbose_name = 'Файл пользователя'
        verbose_name_plural = 'Пользовательские файлы'
