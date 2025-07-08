from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('llamaapi.view_categorisation_benchmark', raise_exception=True)
def categorisation_benchmark(request):
    return render(request, 'categorisation_benchmark.html', {})