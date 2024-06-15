from tqdm import tqdm
import pandas as pd

from django.core.management.base import BaseCommand

from accounts.handlers import DataParser
from accounts.models import Files
from django.core.files.base import File, ContentFile

import os


def is_pdf_file(path):
    extension = path.split('.')[-1]
    return extension == 'pdf'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'input', type=str, help='If dir - will find all .pdf files in this dir. If pdf passed - will parse pdf')

    def handle(self, input, *args, **options):
        paths = []
        if os.path.isdir(input):
            for path in os.listdir(input):
                if is_pdf_file(path):
                    path = os.path.join(input, path)
                    paths.append(path)
        else:
            if is_pdf_file(input):
                paths.append(input)

        # files = []
        for path in tqdm(paths):
            _, filename = os.path.split(path)
            with open(path, 'rb') as f:
                content = ContentFile(f.read())
            # file_obj = File(f)
            file = Files(name=filename)
            file.file.save(filename, content=content)
            # file.file.save(name=None, content=file_obj)
            # files.append(file)
            file.save()
            print(DataParser.pdf_to_data(file, path))

        # [DataParser.pdf_to_data(file) for file in tqdm(files)]
