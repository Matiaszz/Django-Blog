from django.shortcuts import render


def index(req):
    return render(req, 'blog/pages/index.html')
