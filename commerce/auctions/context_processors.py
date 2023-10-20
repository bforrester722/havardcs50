def watch_count(request):
    if request.user.is_authenticated:
        return {"watch_count": request.user.watching.count()}
    else:
        return {"watch_count": 0}
