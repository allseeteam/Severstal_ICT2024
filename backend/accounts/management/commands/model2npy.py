from django.apps import apps
from django.core.management.base import BaseCommand
import numpy as np


class Command(BaseCommand):
    help = ("Output the specified model as numpy array")

    def add_arguments(self, parser):
        parser.add_argument('appmodel', type=str)

    def handle(self, appmodel, *args, **kwargs):
        app_name, model_name = appmodel.split('.')
        model = apps.get_model(app_name, model_name)
        field_names = [f.name for f in model._meta.fields]
        arr = [
            [getattr(instance, f) for f in field_names]
            for instance in model.objects.all()
        ]
        np_arr = np.array(arr)
        np.save(f'{model_name}', np_arr, allow_pickle=True)
