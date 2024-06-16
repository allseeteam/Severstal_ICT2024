from django.forms import model_to_dict

from analyst.celery import app
from analyst.settings import YANDEX_SEARCH_API_TOKEN
from search import ya_search
from extract.reports import get_one_figure_by_entity
from extract import preprocess_entity
from . import models
from .handlers import SiteParser, DataParser


@app.task
def add_data_to_report_block(report_block_id: int, meta_block_id: int):
    process_block(report_block_id, meta_block_id)


@app.task
def add_video_data_to_report_block(report_block_id: int, meta_block_id: int, video_url: str, model_id='yandexgpt'):
    report_block = models.ReportBlock.objects.get(id=report_block_id)
    meta_block = models.MetaBlock.objects.get(id=meta_block_id)
    report = report_block.report
    search_query = f'{meta_block.query_template} {report.search_query} аналитика'
    print(search_query)
    # data = DataParser.summarize_video_id(video_id, model_id)
    data = DataParser.summarize_video(search_query, model_id)
    if data is None:
        report_block.readiness = models.ReportBlock.ERROR
        return
    report_block.data = data
    report_block.representation = {'text': data.data}
    report_block.readiness = models.ReportBlock.READY
    report_block.type = models.ReportBlock.TEXT
    report_block.save()


@app.task
def add_search_data_to_report_block(report_block_id: int, urls_to_parse: str, model_id='yandexgpt'):
    report_block = models.ReportBlock.objects.get(id=report_block_id)

    parser = SiteParser()
    data = parser.parse_pages(urls=urls_to_parse)
    if not data:
        data = DataParser.summarize_urls_from_search(urls_to_parse, model_id)
        if data is None:
            report_block.readiness = models.ReportBlock.ERROR
    if data is None:
        report_block.readiness = models.ReportBlock.ERROR
        return
    for data_obj in data:
        try:
            entity = model_to_dict(data_obj)
            if entity['data_type'] == 'text':
                report_block.data = data_obj
                report_block.representation = {'text': data_obj.data}
                report_block.readiness = models.ReportBlock.READY
                report_block.type = 'text'
                break
            entity['frame'] = entity['data']
            entity['meta'] = entity['meta_data'].get('title', '')
            entity = preprocess_entity(entity)
            representation = get_one_figure_by_entity(
                entity=entity, return_plotly_format=True)
            representation = representation.to_dict()

            report_block.data = data_obj
            report_block.representation = representation
            report_block.type = models.ReportBlock.PLOTLY
            report_block.readiness = models.ReportBlock.READY
            break
        except Exception as e:
            print(e)
    report_block.save()


def process_block(report_block_id: int, meta_block_id: int, model_id='yandexgpt'):
    report_block = models.ReportBlock.objects.get(id=report_block_id)
    meta_block = models.MetaBlock.objects.get(id=meta_block_id)
    report = report_block.report

    search_query = f'{meta_block.query_template} {report.search_query.text} аналитика'
    search = ya_search(
        search_query,
        YANDEX_SEARCH_API_TOKEN
    )

    urls = [r.get('url') for r in search]

    parser = SiteParser()
    data = parser.parse_pages(urls=urls)
    if not data:
        # если в поиске ничего нет, то идем в поиск по видео
        data = DataParser.summarize_video(search_query, model_id)
        if data is None:
            # если там пофейлились, то идем суммаризировать обычный поиск
            data = DataParser.summarize_urls_from_search(urls, model_id)
            if data is None:
                report_block.readiness = models.ReportBlock.ERROR
        if data:
            data = [data]

    report_block.readiness = models.ReportBlock.ERROR
    for data_obj in data:
        try:
            entity = model_to_dict(data_obj)
            if entity['data_type'] == 'text':
                report_block.data = data_obj
                report_block.representation = {'text': data_obj.data}
                report_block.readiness = models.ReportBlock.READY
                report_block.type = 'text'
                break
            print(entity)
            entity['frame'] = entity['data']

            entity['meta'] = entity['meta_data'].get('title', '')

            entity = preprocess_entity(entity)
            representation = get_one_figure_by_entity(
                entity=entity, return_plotly_format=True)
            representation = representation.to_dict()

            report_block.data = data_obj
            report_block.representation = representation
            report_block.type = models.ReportBlock.PLOTLY
            report_block.readiness = models.ReportBlock.READY
            break
        except Exception as e:
            print(e)
            continue

    if report_block.readiness != models.ReportBlock.READY:
        report_block.readiness = models.ReportBlock.ERROR
    report_block.save()
