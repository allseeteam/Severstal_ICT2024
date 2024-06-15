from export.excel import *  # noqa
from export.word import *  # noqa
from export.pdf import *  # noqa
import plotly.graph_objects as go
import plotly
from django.forms import model_to_dict
import markdown


def preprocess_blocks(blocks):  # blocks: list[models.ReportBlock]
    """
    возвращает два объекта
    1. список словарей готовых данных блоков для рендера в ворд и пдф
    2. список датафреймов (которые лежат внутри блоков) - для экселя
    """

    from extract import preprocess_entity, get_table_fig

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
