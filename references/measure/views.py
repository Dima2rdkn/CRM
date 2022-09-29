from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from references.measure.models import Measure
from .forms import MeasureEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class MeasureList(ListView):
    model = Measure
    context_object_name = 'measure'
    template_name = 'references/measure/list.html'


class MeasureCreateView(LoginRequiredMixin, CreateView):
    model = Measure
    form_class = MeasureEditForm
    template_name = 'references/measure/edit.html'

    def get_success_url(self):
        return reverse('measure_list')


class MeasureUpdateView(LoginRequiredMixin, UpdateView):
    model = Measure
    form_class = MeasureEditForm
    template_name = 'references/measure/edit.html'

    def get_success_url(self):
        return reverse('measure_list')


class MeasureDeleteView(LoginRequiredMixin, DeleteView):
    model = Measure
    context_object_name = 'measure'
    template_name = 'references/measure/delete.html'

    def get_success_url(self):
        return reverse('measure_list')
