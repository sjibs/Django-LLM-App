from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from llamaapi.google_sheets import get_sheet_headings
from django.shortcuts import render
from llamaapi.google_sheets import get_google_sheets_data

@permission_required('llamaapi.view_categorisation_benchmark', raise_exception=True)

def categorisation_benchmark(request):
    sheet_heading_data = get_sheet_headings()
    if request.method == "POST":
        # Get the submitted data from the form
        table_heading = request.POST.get("table_heading")
        system_prompt = request.POST.get("system_prompt")

        # Fetch and process data from Google Sheets
        processed_reviews = get_google_sheets_data(table_heading)

        # Prepare processed data object
        processed_data = {
            "processed_reviews": processed_reviews,
            "selected_prompt": system_prompt,
            "selected_heading": table_heading,
        }

        # Render the template with processed data
        return render(request, "categorisation_benchmark.html", {"processed_data": processed_data, "sheet_data": sheet_heading_data})

    return render(request, 'categorisation_benchmark.html', {'sheet_data': sheet_heading_data})