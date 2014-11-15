
def when_updated(request):
    updated = ''
    user = request.user
    if user.is_authenticated():
        duser = user.duser_set.only()
        if duser:
            updated = duser[0].updated
    return {'updated': updated}
