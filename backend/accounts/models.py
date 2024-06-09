from django.db import models


class SearchQuery(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='search_queries',
        verbose_name='Пользователь',
        null=True
    )
    text = models.TextField(
        'Текст запроса пользователя',
        max_length=400
    )
    updates_subscribe = models.BooleanField(
        'Подписка на обновления',
        default=False
    )
    data = models.ManyToManyField(
        'Data',
        verbose_name='Данные',
        related_name='search_queries'
    )

    class Meta:
        verbose_name = 'Поисковый запрос'
        verbose_name_plural = 'Поисковые запросы'

    def __str__(self) -> str:
        return f'Пользовательский запрос: {self.text}'
    

class Account(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='accounts',
        verbose_name='Пользователь',
        null=True
    )
    search_query = models.ForeignKey(
        'SearchQuery',
        on_delete=models.SET_NULL,
        related_name='accounts',
        verbose_name='Поисковый запрос',
        null=True
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    data = models.ManyToManyField(
        'Data',
        verbose_name='Данные',
        related_name='accounts'
    )

    class Meta:
        verbose_name = 'Аналитический отчет'
        verbose_name_plural = 'Аналитические отчеты'


class Data(models.Model):
    WEB_PAGE = 'web_page'
    VIDEO = 'video'
    FILE = 'file'

    SOURCE_TYPES = (
        (WEB_PAGE, 'Страница в интернете'),
        (VIDEO, 'Видео'),
        (FILE, 'Пользовательский файл'),
    )

    SERIES = 'series'
    REFERENCE = 'reference'

    DATA_TYPES = (
        (SERIES, 'Временной ряд'),
        (REFERENCE, 'Справочник')
    )

    type = models.CharField(
        'Тип источника данных',
        choices=SOURCE_TYPES,
        max_length=16
    )
    url = models.CharField(
        'URL',
        max_length=1024,
        blank=True
    )
    file = models.OneToOneField(
        'UserFiles',
        on_delete=models.SET_NULL,
        related_name='data',
        verbose_name='Пользовательский файл',
        null=True
    )
    data_type = models.CharField(
        'Тип данных',
        choices=DATA_TYPES,
        max_length=16
    )
    meta_data = models.JSONField(
        verbose_name='Мета данные'
    )
    data = models.JSONField(
        verbose_name='Данные'
    )
    date = models.DateTimeField(
        'Дата создания версии',
    )
    version = models.PositiveIntegerField(
        'Версия'
    )

    class Meta:
        verbose_name = 'Данные'
        verbose_name_plural = 'Данные'


class WebPage(models.Model):
    url = models.CharField(
        'URL',
        max_length=1024,
        unique=True
    )
    content = models.TextField(
        'Содержание страницы',
        blank=True
    )
    update_date = models.DateTimeField(
        'Дата обновления',
        null=True
    )


    class Meta:
        verbose_name = 'Интернет страница'
        verbose_name_plural = 'Интернет страницы'

    def __str__(self) -> str:
        return self.url


class UserFiles(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='files',
        verbose_name='Пользователь',
        null=True
    )
    name = models.CharField(
        'Название файла'
    )
    file = models.FileField(
        upload_to='files/'
    )

    class Meta:
        verbose_name = 'Файл пользователя'
        verbose_name_plural = 'Пользовательские файлы'
