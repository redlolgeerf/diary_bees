
def when_updated(request):
    updated = ''
    user = request.user
    if user.is_authenticated():
        duser = user.duser_set.only()[0]
        if duser:
            updated = duser.updated
    return {'updated': updated}
