from django.db import models

class CategorisationBenchmark(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        permissions = [
            ("view_categorisation_benchmark", "Can view categorisation benchmark"),
        ]