from datetime import datetime
from django.conf import settings
from bees.models import DUser, AuthorisationRequest, Bees
from bees.grabber import Grabber


def check_my_bees():
    all_requests = AuthorisationRequest.objects.all()
    my_id = settings.MY_DIARY_ID
    grab = Grabber()
    my_bees = Bees(grab.get_bees(my_id)).to_dict()
    for request in all_requests:
        if request.duser in my_bees:
            duser = DUser.objects.get(d_id=request.duser)
            duser.confirmed = True
            duser.save()
            request.delete()

    # delete too old requests
    request_lifetime = settings.REQUEST_LIFETIME
    cut_off = datetime.now() - request_lifetime
    all_requests = AuthorisationRequest.objects.filter(created__lte=cut_off)
    for request in all_requests:
        request.delete()


def update_bees():
    diary_users = DUser.objects.all()
    grab = Grabber()
    for d_user in diary_users:
        new_bees = grab.get_bees(d_user.d_id)
        d_user.update_bees(new_bees)
        d_user.save()
