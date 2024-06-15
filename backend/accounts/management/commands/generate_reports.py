from django.core.management.base import BaseCommand
from accounts import models
from export import save_excel_report, save_pdf_report, save_word_report, preprocess_blocks


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
        new_blocks, tables = preprocess_blocks(blocks)
        save_pdf_report(new_blocks, 'output_report.pdf')
        save_word_report(new_blocks, 'output_report.docx')
        save_excel_report(tables, 'output_report.xlsx')
