def custom_cas_login(request, *args, **kwargs):
    """If a student has not completed the welcome walkthrough, go there on login."""
    response = cas_login(request, *args, **kwargs)
    # returns HttpResponseRedirect

    if request.user.is_authenticated():

        if not request.user.student.totally_done():

            if not request.user.student.completedName:
                return HttpResponseRedirect(reverse('welcomeName'))
            elif not request.user.student.completedPrivacy:
                return HttpResponseRedirect(reverse('welcomePrivacy'))
            elif not request.user.student.completedMajor:
                return HttpResponseRedirect(reverse('welcomeMajor'))
            elif not request.user.completedSocial:
                return HttpResponseRedirect(reverse('welcomeSocial'))
        else:
            welcome_back = random.choice(return_messages)
            messages.add_message(request, messages.INFO, mark_safe(welcome_back))

    return response


# only two students on the same floor can confirm one another (crowdsourced verification)
def on_the_same_floor(student, confirmer):
    if student == confirmer:
        # Student is confirmer
        return False
    student_floor = student.get_floor()
    confirmer_floor = confirmer.get_floor()
    # room hasn't been set yet
    if (student_floor is None) or (confirmer_floor is None):
        # one Student is None
        return False
    elif not(student_floor == confirmer_floor):
        # not the same floor
        return False
    else:
        return True


def pk_or_none(me, obj):
    if obj is None:
        return None
    else:
        return obj.pk


def create_email(text_path, html_path, subject, to, context):
    text_email = get_template(text_path)
    html_email = get_template(html_path)

    email_context = Context(context)

    from_email, cc = ('noreply@srct.gmu.edu',
                      '')

    text_content = text_email.render(email_context)
    html_content = html_email.render(email_context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [cc])
    # mime multipart requires attaching text and html in this order
    msg.attach_alternative(html_content, 'text/html')
    return msg


def no_nums(name):
    no_numbers = re.sub('[0-9]', '', name)
    return no_numbers



def get_semester(date):
    # months are between 1 and 12, inclusive
    semesters = {
        'Spring': (1, 2, 3, 4, 5),
        'Summer': (6, 7),
        'Fall': (8, 9, 10, 11, 12)
    }

    for semester, months in semesters.iteritems():
        if date.month in months:
            semester_string = semester

    return semester_string


# this should be written in cache, to be entirely honest
def shadowbanning(me, other_people):
    # start with only students who are actually blocking anyone
    blockers = [student for student in Student.objects.exclude(blocked_kids=None)]
    # of those students, collect the ones that block *you*
    blocks_me = [student
                 for student in blockers
                 if me in student.blocked_kids.all()]
    if blocks_me:  # python implicit truth evaluation
        student_safety = list(set(other_people) - set(blocks_me))
        return student_safety
    else:
        return other_people
