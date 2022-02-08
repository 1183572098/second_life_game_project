from django.http import HttpResponse


def index(request):
    print("This is index page")
    return HttpResponse("This is index Page. Testing")
