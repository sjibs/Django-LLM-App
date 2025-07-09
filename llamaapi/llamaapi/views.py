from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from llamaapi.google_sheets import get_sheet_headings, get_google_sheets_data
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import base64

@permission_required('llamaapi.view_categorisation_benchmark', raise_exception=True)
def categorisation_benchmark(request):
    sheet_heading_data = get_sheet_headings()
    spreadsheet_id = os.getenv('ASSESSMENT_SPREADSHEET_ID')

    if request.method == "POST":
        # Get the submitted data from the form
        table_heading = request.POST.get("table_heading")
        system_prompt = request.POST.get("system_prompt")

        # Fetch and process data from Google Sheets
        processed_reviews = get_google_sheets_data(table_heading)

        # Calculate accuracy metrics
        correct_count = sum(1 for review in processed_reviews if review["isCorrect"])
        total_count = len(processed_reviews)
        accuracy_percentage = (correct_count / total_count * 100) if total_count > 0 else 0

        # Generate pie chart
        def generate_pie_chart(correct_count, total_count):
            labels = ['Correct', 'Incorrect']
            sizes = [correct_count, total_count - correct_count]
            colors = ['#6a0dad', '#ccc']
            explode = (0.1, 0)  # Explode the 'Correct' slice

            plt.figure(figsize=(6, 4))
            plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

            # Save the chart to a BytesIO object
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            chart_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()

            return chart_base64

        pie_chart = generate_pie_chart(correct_count, total_count)

        # Prepare processed data object
        processed_data = {
            "processed_reviews": processed_reviews,
            "selected_prompt": system_prompt,
            "selected_heading": table_heading,
            "accuracy_percentage": accuracy_percentage,
            "correct_count": correct_count,
            "total_count": total_count,
            "pie_chart": pie_chart,
        }

        # Render the template with processed data
        return render(request, "categorisation_benchmark.html", {"processed_data": processed_data, "sheet_data": sheet_heading_data,'spreadsheet_id': spreadsheet_id,})

    return render(request, 'categorisation_benchmark.html', {'sheet_data': sheet_heading_data, 'spreadsheet_id': spreadsheet_id,})