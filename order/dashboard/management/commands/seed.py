from django.core.management.base import BaseCommand, CommandError
from ...models import GlobalSiteSetting

class Command(BaseCommand):
    help = "Populates the database with default settings. Intended to be used once on project initialization."

    def handle(self, *args, **options):
        GlobalSiteSetting.objects.get_or_create(
            key = "EMAIL_MESSAGE",
            value = "Thank you for your purchase! Your order will be available for pickup at this weeks market."
        )
        print("Seeded setting EMAIL_MESSAGE")

        GlobalSiteSetting.objects.get_or_create(
            key = "EMAIL_SUBJECT",
            value = "Thank you for your purchase! Here's your Conecopia Gelato Reciept."
        )
        print("Seeded setting EMAIL_SUBJECT")

        GlobalSiteSetting.objects.get_or_create(
            key = "EMAIL_SENDER",
            value = "noreply@conecopia.com"
        )
        print("Seeded setting EMAIL_SENDER")

        GlobalSiteSetting.objects.get_or_create(
            key = "EMAIL_CC",
            value = "conecopiagelato@gmail.com"
        )
        print("Seeded setting EMAIL_EMAIL_CC")