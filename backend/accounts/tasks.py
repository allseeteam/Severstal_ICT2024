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


def process_block(report_block_id: int, meta_block_id: int):
    report_block = models.ReportBlock.objects.get(id=report_block_id)
    meta_block = models.MetaBlock.objects.get(id=meta_block_id)
    report = report_block.report

    search = ya_search(
        f'{meta_block.query_template} {report.search_query.text} аналитика',
        YANDEX_SEARCH_API_TOKEN
    )

    urls = [r.get('url') for r in search]

    parser = SiteParser()
    data = parser.parse_pages(urls=urls)
    if not data:
        best_data = None
        for url in urls:
            try:
                data_row = DataParser.summarize_url(url)
                if 'сменим тему' in data_row.data or len(data_row.data) < 50:
                    continue
                best_data = data_row
            except Exception:
                pass
        if best_data:
            data = [best_data]
        else:
            report_block.readiness = models.ReportBlock.ERROR
            return
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
            representation = get_one_figure_by_entity(entity=entity, return_plotly_format=True)
            representation = representation.to_dict()

            report_block.data = data_obj
            report_block.representation = representation
            report_block.type = 'plotly'
            report_block.readiness = models.ReportBlock.READY
            break
        except Exception as e:
            print(e)
            continue

    report_block.save()
