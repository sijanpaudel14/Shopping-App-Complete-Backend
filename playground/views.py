from math import log
from django.shortcuts import render
from django.core.cache import cache
from django.core.mail import EmailMessage, BadHeaderError
from django.utils.decorators import method_decorator
from .tasks import notify_customers
from django.views.decorators.cache import cache_page
import requests
from rest_framework.views import APIView
# To prevent from interception, we use BadHeaderError while sending email so that no one can inject headers in the email.

from templated_mail.mail import BaseEmailMessage


# def say_hello(request):
#     try:
# # this is for site admins
# mail_admins('subject', 'message',
#             html_message='<h1>This is an important message</h1>')
# # this is for general email sending
# send_mail('subject', 'message',
#           'info@sijanbuy.com', ['bob@sijanbuy.com'])
# message = EmailMessage('subject','message','sijan@buy.com',['hi@buy.com', 'hello@buy.com','hihello@buy.com'])
# message.attach_file('playground/static/images/image.png')
# message.send()

# message = BaseEmailMessage(
#     template_name='emails/hello.html',
#     context={
#         'name': "Sijan"
#     }
# )
# message.send(['hello@buy.com'])
# except BadHeaderError:
#     pass
# def say_hello(request):
#     notify_customers.delay('Hello')
#     return render(request, 'hello.html', {'name': 'Sijjan'})

# def say_hello(request):
#     key = 'httpbin_response'
#     if cache.get(key) is None:
#         print("Making external API call")
#         response = requests.get('https://httpbin.org/delay/2')
#         data = response.json()
#         cache.set(key, data)  # Cache for 30 seconds
#     return render(request, 'hello.html', {'name': 'Sijan', 'data': cache.get(key)})

# @cache_page(30)  # Cache the entire view for 30 seconds
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'hello.html', {'name': 'Sijan', 'data': data})

# If any changes is made in the view, the cache will be invalidated automatically. so, our changes will be reflected only after TIMEOUT of cache.

# To manually clear the cache, you can use:
# from django.core.cache import cache
# cache.clear()

# To clear specific cache key, you can use:
# cache.delete('httpbin_response')

# For class, cache_page doesn't work directly. We need to use method_decorator to apply it to dispatch method of the class-based view.

import logging

logger = logging.getLogger(__name__)  ## playground.views


class HelloView(APIView):
    # @method_decorator(cache_page(5 * 60))  # Cache the view for 5 minutes
    def get(self, request):
        try:
            logger.info("Fetching data from external API")
            response = requests.get('https://httpbin.org/delay/1')
            logger.info("Received response from external API")
            data = response.json()
        except Exception as e:
            logger.critical(f"Error fetching data from external API: {e}")
        return render(request, 'hello.html', {'name': 'Sijan', 'data': "Sijan"})
