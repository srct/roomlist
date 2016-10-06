from django.core.management.base import BaseCommand
from accounts.models import Student


class Command(BaseCommand):
    args = ""
    help = "Deletes all students' rooms at the end of the semester"

    def handle(self, *args, **kwargs):
        count = 0
        for student in Student.objects.all():
            student.room = None
            count += 1

        self.stdout.write("Successfully overwrote %d student room(s)." % count)
