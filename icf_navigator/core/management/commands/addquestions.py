from django.core.management.base import BaseCommand, CommandError
from core.models import *

class Command(BaseCommand):
    help = 'Adds all pre-configured questions to database'

    def handle(self, *args, **options):
        FreeTextQuestion.objects.get_or_create(
            order=1.0,
            label="study_title",
            text="What is the full title of your study?")
        FreeTextQuestion.objects.get_or_create(
            order=1.5,
            label="study_about",
            text="What is this study about?")
        ContactQuestion.objects.get_or_create(
            order=2.0,
            label="primary_contact",
            text="Who is the primary contact for the study?"
        )
        IntegerQuestion.objects.get_or_create(
            order=3.0,
            label="visits_required",
            text="How many visits will be required?"
        )
        FreeTextQuestion.objects.get_or_create(
            order=3.1,
            label="visit_length",
            text="How long will each visit take? e.g. 5 hours")
        FreeTextQuestion.objects.get_or_create(
            order=3.2,
            label="prep_time",
            text="How much prep time will  be required for each visit? e.g. 5 hours")
        TextListQuestion.objects.get_or_create(
            order=5.0,
            label="joining_risks",
            text="What are the risks of joining?",
            minimum_required=3
        )
        TextListQuestion.objects.get_or_create(
            order=6.0,
            label="research_features",
            text="What are the aspects of the study?",
            minimum_required=3
        )
        YesNoExplainQuestion.objects.get_or_create(
            order=7.0,
            text="Will the participant’s regular medical treatments change by joining this study?",
            label="change_regular_medical_treatments",
            explain_when="Y"
        )
