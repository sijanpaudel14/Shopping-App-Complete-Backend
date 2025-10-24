from django.shortcuts import render
from django.core.cache import cache
from django.core.mail import EmailMessage, BadHeaderError
from .tasks import notify_customers

import requests
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

def say_hello(request):
    key = 'httpbin_response'
    if cache.get(key) is None:
        print("Making external API call")
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        cache.set(key, data)  # Cache for 30 seconds
    return render(request, 'hello.html', {'name': 'Sijan', 'data': cache.get(key)})