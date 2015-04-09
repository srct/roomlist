from django.contrib.auth.models import User

from accounts.models import Student

from django.conf import settings

def create_user(tree):

    username = tree[0][0].text
    user, user_created = User.objects.get_or_create(username=username)

    if user_created:
        user.email = "%s@%s" % (username, settings.ORGANIZATION_EMAIL_DOMAIN)
        user.save()
        new_student = Student.objects.create(user=user)
        new_student.save()

        print("Created user %s!" % username)
