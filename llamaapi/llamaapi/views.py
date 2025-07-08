from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from llamaapi.google_sheets import get_google_sheets_data

@permission_required('llamaapi.view_categorisation_benchmark', raise_exception=True)
def categorisation_benchmark(request):
    sheet_data = get_google_sheets_data('Sheet1!A1:D5')
    return render(request, 'categorisation_benchmark.html', {'sheet_data': sheet_data})