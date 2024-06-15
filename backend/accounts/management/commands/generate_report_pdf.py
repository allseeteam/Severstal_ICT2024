from django.core.management.base import BaseCommand
from accounts import models

import plotly
import plotly.graph_objs as go
from extract import get_table_fig, preprocess_entity
from xhtml2pdf import pisa
from django.forms import model_to_dict



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('report_id', type=str, help='Input csv')

    def handle(self, report_id, *args, **options):
        report = models.Report.objects.filter(id=report_id).first()
        print(report.id)
        blocks = models.ReportBlock.objects.filter(report_id=report.id).all()
        blocks = [blocks[0], blocks[0]]
        print(len(blocks))
        paths = []
        for block in blocks:
            data = block.data
            
            type = block.type
            if type == 'plotly':
                representation = block.representation
                entity = model_to_dict(data)
                entity['frame'] = entity['data']
                entity['meta'] = entity['meta_data'].get('title', '')
                entity = preprocess_entity(entity)
                table = get_table_fig(entity)
                fig = go.Figure(representation)
                filename = f'block_{block.id}'
                filename_table = f'block_{block.id}_table'
                plotly.io.write_image(fig, filename, format='jpg')
                plotly.io.write_image(table, filename_table, format='jpg')
                paths.append([filename, filename_table])
            else:
                print('text, not plotly obj')
        static_report = ''
        for fig, fig_table in paths:
            static_report += report_block_template(fig, fig_table, caption='')
        convert_html_to_pdf(static_report, 'output_report.pdf')


def report_block_template(fig, caption=''):
    graph_block = (''
                   '<div>'
                   '<img style="height: 400px;" src="{fig}.jpg">'
                   '<img style="height: 400px;" src="{fig_table}.jpg">'
                   '</div>'
                   # '</a>'
                   )

    report_block = ('' +
                    graph_block +
                    '{caption}' +  # Optional caption to include below the graph
                    '<br>' +  # Line break
                    '<a href="{fig}" style="color: rgb(190,190,190); text-decoration: none; font-weight: 200;" target="_blank">' +
                    # Direct readers to Plotly for commenting, interactive graph
                    # 'Click to comment and see the interactive graph' +
                    '</a>' +
                    '<br>' +
                    '<hr>')  # horizontal line

    return report_block.format(fig=fig, caption=caption)


# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        source_html,                # the HTML to convert
        dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return True on success and False on errors
    return pisa_status.err
