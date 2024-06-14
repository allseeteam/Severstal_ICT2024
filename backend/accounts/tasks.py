from django.forms import model_to_dict

from analyst.celery import app
from extract.reports import get_one_figure_by_entity
from . import models
from .handlers import SiteParser

@app.task
def add_data_to_report_block(report_block_id: int, meta_block_id: int):
    report_block = models.ReportBlock.objects.get(id=report_block_id)
    meta_block = models.MetaBlock.objects.get(id=meta_block_id)
    report = report_block.report

    urls = [] # тут из яндекс поиска ссылки будем получать

    parser = SiteParser()
    data = parser.parse_pages(urls=urls)
    if len(data) == 0:
        report_block.readiness = models.ReportBlock.ERROR
    else:
        data_obj = data[0]
        report_block.data = data_obj

        entity = model_to_dict(data_obj)
        entity['frame'] = entity['data']
        entity['meta'] = entity['meta_data']['title']
        representation=get_one_figure_by_entity(entity=entity)

        report_block.representation = representation
        report_block.readiness = models.ReportBlock.READY

    report_block.save()
