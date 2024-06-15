from django.core.management.base import BaseCommand
from accounts import models

import plotly
import plotly.graph_objs as go
from extract import get_table_fig, preprocess_entity
from export import save_excel_report, save_pdf_report, save_word_report

from django.forms import model_to_dict
import markdown


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('report_id', type=str, help='Input csv')

    def handle(self, report_id, *args, **options):
        report = models.Report.objects.filter(id=report_id).first()
        blocks = models.ReportBlock.objects.filter(report_id=report.id).all()
        if not blocks:
            print('Нет блоков по такому id')
            return
        blocks = [blocks[0], blocks[0]]  # для теста. в проде закомментить.
        new_blocks, tables = save_blocks_to_jpg(blocks)
        save_pdf_report(new_blocks, 'output_report.pdf')
        save_word_report(new_blocks, 'output_report.docx')
        save_excel_report(tables, 'output_report.xlsx')


def save_blocks_to_jpg(blocks):
    """
    возвращает два объекта
    1. список словарей готовых данных блоков для рендера в ворд и пдф
    2. список датафреймов (которые лежат внутри блоков) - для экселя
    """
    tables = []
    new_blocks = []
    for i, block in enumerate(blocks):
        data = block.data
        source = data.page.url
        type = block.type
        if type == 'plotly':
            representation = block.representation
            entity = model_to_dict(data)
            entity['frame'] = entity['data']
            entity['meta'] = entity['meta_data'].get('title', '')
            entity = preprocess_entity(entity)
            table = get_table_fig(entity)
            fig = go.Figure(representation)
            filename = f'block_{block.id}.jpg'
            filename_table = f'block_{block.id}_table.jpg'
            plotly.io.write_image(fig, filename, format='jpg')
            plotly.io.write_image(table, filename_table, format='jpg')
            tables.append(entity['frame'])
            new_blocks.append({
                'path_fig': filename,
                'path_table': filename_table,
                'type': 'plotly',
                'source': source,
                'position': i,
            })
        else:
            new_blocks.append({
                'text': data.data,
                'html_text': markdown.markdown(data.data),
                'type': 'text',
                'source': source,
                'position': i,
            })
    return new_blocks, tables
