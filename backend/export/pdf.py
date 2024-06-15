from xhtml2pdf import pisa
from io import StringIO


def save_pdf_report(blocks: dict, output_path):
    static_report = ''
    for block in blocks:
        source = block['source']
        if block['type'] == 'plotly':
            fig, fig_table = block['path_fig'], block['path_table']
            static_report += report_block_template(
                fig, fig_table, source, caption='')
        elif block['type'] == 'text':
            text = block['html_text']
            static_report += report_text_block_template(text, source)
    convert_html_to_pdf(static_report, output_path)


def convert_html_to_pdf(source_html, output_filename):
    path_to_helvetica = 'helvetica.ttf'
    print(path_to_helvetica)
    source_html = """
    <html>
    <head>
    <title>Отчет</title>
    <style>
    @font-face {
        font-family: Helvetica;
        src: url(""" + f'"{path_to_helvetica}"' + """);
    }

    .inner {
        margin-top: 400px;
        align-text: center;
    }
    h1 {
        margin-left: 200px;
    }
    h2 {
        margin-left: 250px
    }
    h3 {
        margin-left: 250px;
    }
    </style>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    </head>
    """ + f"""
    <body>
        <div id="outer">
            <h2 class="inner">Титульный лист</h2>
            <h1 class="inner" style="font-size:40px">Аналитический отчет</h1>
            <h3 class="inner">Тут мог быть ваш корпоративный шаблон</h3>
            <div>
                <pdf:nextpage /> 
            </div> 
        </div>
    {source_html}
    </body>
    </html>
    """
    print(source_html)
    result_file = open(output_filename, "w+b")

    pisa_status = pisa.CreatePDF(
        StringIO(source_html),
        dest=result_file,
        encoding='utf-8'
    )
    result_file.close()
    return pisa_status.err


def report_block_template(fig, fig_table, source, caption=''):
    graph_block = (
        ''
        '<div>'
        # f'<img style="height: 400px; width: 800px;" src="{fig}">'
        f'<img src="{fig}">'
        '</div>'
        '<br>'
        '<div>'
        # f'<img style="height: 400px; width: 800px;" src="{fig_table}">'
        f'<img src="{fig_table}">'
        '</div>'
        f'<h3>Источник:<a href="{source}">{source}</a></h3>'
        '<div>'
        '<pdf:nextpage />'
        '</div> '
    )
    return graph_block


def report_text_block_template(text, source):
    report_block = (
        ''
        '<div style="  display: flex;align-items: center;justify-content: center;">'
        f'{text}'
        '</div>'
        f'<h3>Источник:<a href="{source}">{source}</a></h3>'
        '<div>'
        '<pdf:nextpage />'
        '</div> '
    )
    return report_block
