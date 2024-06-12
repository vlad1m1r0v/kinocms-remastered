from ajax_datatable.views import AjaxDatatableView
from django.http import HttpRequest

from .models import Hall


class AdminHallsDataTableView(AjaxDatatableView):
    model = Hall
    title = 'Halls'
    initial_order = [["id", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'id', 'title': 'ID', 'visible': True, },
        {'name': 'name_en', 'title': 'Name', 'visible': True, },
        {'name': 'created_at', 'title': 'Creation Date', 'visible': True, },
    ]

    def get_initial_queryset(self, request: HttpRequest = None):
        queryset = self.model.objects.all()
        cinema_id = int(request.REQUEST.get(key='cinema_id'))
        queryset = queryset.filter(cinema_id=cinema_id)
        return queryset
