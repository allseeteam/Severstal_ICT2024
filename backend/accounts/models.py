import io

from django.core.files.base import ContentFile
from django.db import models
from export import preprocess_blocks, save_pdf_report, save_excel_report, save_word_report

class Site(models.Model):
    domain = models.CharField(
        'Домен'
    )

    class Meta:
        verbose_name = 'Проверенный сайт'
        verbose_name_plural = 'Проверенные сайты'

    def __str__(self) -> str:
        return self.domain


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
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'text'],
                name='%(app_label)s_%(class)s_uniq'
            )
        ]

    def __str__(self) -> str:
        return f'Пользовательский запрос: {self.text}'


class Theme(models.Model):
    name = models.CharField(
        'Название'
    )

    class Meta:
        verbose_name = 'Тематика отчета'
        verbose_name_plural = 'Тематики отчетов'

    def __str__(self) -> str:
        return self.name


class Template(models.Model):
    name = models.CharField(
        'Название'
    )
    theme = models.ForeignKey(
        'Theme',
        on_delete=models.SET_NULL,
        related_name='templates',
        verbose_name='Тематика отчета',
        null=True
    )

    class Meta:
        verbose_name = 'Шаблон отчета'
        verbose_name_plural = 'Шаблоны отчетов'

    def __str__(self) -> str:
        return self.name


class MetaBlock(models.Model):
    PLOTLY = 'plotly'
    TEXT = 'text'
    TYPES = (
        (PLOTLY, 'Plotly'),
        (TEXT, 'Текст')
    )

    query_template = models.CharField(
        'Шаблон запроса'
    )
    template = models.ForeignKey(
        'Template',
        on_delete=models.CASCADE,
        related_name='meta_blocks',
        verbose_name='Шаблон отчета'
    )
    type = models.CharField(
        'Тип',
        choices=TYPES
    )
    position = models.PositiveIntegerField(
        'Позиция'
    )

    class Meta:
        verbose_name = 'Мета-блок отчета'
        verbose_name_plural = 'Мета-блоки отчетов'

    def __str__(self) -> str:
        return self.query_template


class Report(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='reports',
        verbose_name='Пользователь',
        null=True
    )
    search_query = models.ForeignKey(
        'SearchQuery',
        on_delete=models.SET_NULL,
        related_name='reports',
        verbose_name='Поисковый запрос',
        null=True
    )
    template = models.ForeignKey(
        'Template',
        on_delete=models.SET_NULL,
        verbose_name='Шаблон',
        null=True
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    data = models.ManyToManyField(
        'Data',
        through='ReportBlock',
        verbose_name='Данные',
        related_name='reports'
    )

    class Meta:
        verbose_name = 'Аналитический отчет'
        verbose_name_plural = 'Аналитические отчеты'

    def get_pdf(self):
        blocks = self.blocks.filter(readiness=ReportBlock.READY)
        if not blocks:
            return
        new_blocks, tables = preprocess_blocks(blocks)
        filename = f'report_{self.pk}.pdf'
        save_pdf_report(new_blocks, filename)
        with open(filename, 'rb') as f:
            content = ContentFile(f.read())
        return content

    def get_word(self):
        blocks = self.blocks.filter(readiness=ReportBlock.READY)
        if not blocks:
            return
        new_blocks, tables = preprocess_blocks(blocks)
        filename = f'report_{self.pk}.docx'
        save_word_report(new_blocks, filename)
        with open(filename, 'rb') as f:
            content = ContentFile(f.read())
        return content

    def get_excel(self):
        blocks = self.blocks.filter(readiness=ReportBlock.READY)
        if not blocks:
            return
        new_blocks, tables = preprocess_blocks(blocks)
        filename = f'report_{self.pk}.xlsx'
        save_excel_report(tables, filename)
        with open(filename, 'rb') as f:
            content = ContentFile(f.read())
        return content

class ReportBlock(models.Model):
    READY = 'ready'
    NOT_READY = 'not_ready'
    ERROR = 'error'
    READINESS_STATUSES = (
        (READY, 'Готов'),
        (NOT_READY, 'Не готов'),
        (ERROR, 'Ошибка')
    )

    PLOTLY = 'plotly'
    TEXT = 'text'
    TYPES = (
        (PLOTLY, 'Plotly'),
        (TEXT, 'Текст')
    )

    report = models.ForeignKey(
        'Report',
        on_delete=models.CASCADE,
        related_name='blocks',
        verbose_name='Отчет'
    )
    data = models.ForeignKey(
        'Data',
        on_delete=models.SET_NULL,
        related_name='report_blocks',
        verbose_name='Данные',
        null=True
    )
    representation = models.JSONField('Представление')
    type = models.CharField(
        'Тип',
        choices=TYPES
    )
    comment = models.TextField(
        'Комментарий',
        blank=True
    )
    summary = models.TextField(
        'Вывод LLM',
        blank=True
    )
    readiness = models.CharField(
        'Готовность',
        choices=READINESS_STATUSES
    )
    position = models.PositiveIntegerField(
        'Позиция'
    )


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
    TEXT = 'text'

    DATA_TYPES = (
        (SERIES, 'Временной ряд'),
        (REFERENCE, 'Справочник'),
        (TEXT, 'Текст')
    )

    index_id = models.CharField(
        unique=True,
    )
    type = models.CharField(
        'Тип источника данных',
        choices=SOURCE_TYPES,
    )
    page = models.ForeignKey(
        'WebPage',
        on_delete=models.SET_NULL,
        related_name='data',
        verbose_name='Интернет страницы',
        null=True
    )
    file = models.ForeignKey(
        'Files',
        on_delete=models.SET_NULL,
        related_name='data',
        verbose_name='Пользовательский файл',
        null=True
    )
    data_type = models.CharField(
        'Тип данных',
        choices=DATA_TYPES,
        # max_length=16
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
    title = models.CharField(
        'Title'
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


class Files(models.Model):
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
