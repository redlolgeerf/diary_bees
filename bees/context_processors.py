
def when_updated(request):
    updated = ''
    d_id = ''
    user = request.user
    if user.is_authenticated():
        duser = user.duser_set.only()
        if duser:
            updated = duser[0].updated
            d_id = duser[0].d_id
    return {'updated': updated, 'd_id': d_id}
