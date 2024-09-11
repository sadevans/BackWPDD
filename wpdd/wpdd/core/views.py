from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect

import logging
logging.basicConfig(
                    format = '%(asctime)s [%(name)-20s] %(levelname)-8s %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger('views.py')
logger.setLevel(logging.DEBUG)


def start_page(request):
    return render(request, 'start_page.html')





def chat(request):
    return render(request, 'chat.html')

# def home(request):
#     # Render the home template instead of redirecting
#     return render(request, 'home.html')
