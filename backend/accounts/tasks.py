from django.forms import model_to_dict

from analyst.celery import app
from analyst.settings import YANDEX_SEARCH_API_TOKEN
from search import ya_search
from extract.reports import get_one_figure_by_entity
from . import models
from .handlers import SiteParser

@app.task
def add_data_to_report_block(report_block_id: int, meta_block_id: int):
    report_block = models.ReportBlock.objects.get(id=report_block_id)
    meta_block = models.MetaBlock.objects.get(id=meta_block_id)
    report = report_block.report
    
    search = ya_search(
        f'{meta_block.query_template} {report.search_query.text}',
        YANDEX_SEARCH_API_TOKEN
    )

    urls = [r.get('url') for r in search]

    parser = SiteParser()
    data = parser.parse_pages(urls=urls)
    report_block.readiness = models.ReportBlock.ERROR
    for data_obj in data:
        try:
            entity = model_to_dict(data_obj)
            entity['frame'] = entity['data']
            entity['meta'] = entity['meta_data']['title']
            representation=get_one_figure_by_entity(
                entity=entity,
                return_plotly_format=True if meta_block.type == models.MetaBlock.PLOTLY else False
            )
            
            report_block.data = data_obj
            report_block.representation = representation
            report_block.readiness = models.ReportBlock.READY
            break
        except Exception as e:
            print(e)
            continue

    report_block.save()
