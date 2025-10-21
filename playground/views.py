from django.shortcuts import render
from django.core.mail import EmailMessage, BadHeaderError
# To prevent from interception, we use BadHeaderError while sending email so that no one can inject headers in the email.


def say_hello(request):
    try:
        # # this is for site admins
        # mail_admins('subject', 'message',
        #             html_message='<h1>This is an important message</h1>')
        # # this is for general email sending
        # send_mail('subject', 'message',
        #           'info@sijanbuy.com', ['bob@sijanbuy.com'])
        message = EmailMessage('subject','message','sijan@buy.com',['hi@buy.com', 'hello@buy.com','hihello@buy.com'])
        message.attach_file('playground/static/images/image.png')
        message.send()
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
