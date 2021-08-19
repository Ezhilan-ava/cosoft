from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework import renderers

from paws.users.models import User

#
# def push_message(customer_id, title, body, text):
#     customer = User.objects.get(id=customer_id)
#     android_dict = text
#     android_dict['e_title'] = title
#     android_dict['e_body'] = body
#     if customer.os_type == "android":
#         device = GCMDevice.objects.filter(user=customer).order_by('-date_created').first()
#         if GCMDevice.objects.filter(user=customer).order_by('-date_created').exists():
#             try:
#                 device.send_message(None, extra=android_dict)
#                 resu = "sent"
#             except Exception as e:
#                 resu = str(e)
#
#     if customer.os_type == "ios":
#         device = APNSDevice.objects.filter(user=customer).order_by('-date_created').first()
#         if APNSDevice.objects.filter(user=customer).order_by('-date_created').exists():
#             try:
#                 device.send_message(message={"title": title,
#                                              "body": body},
#                                     sound='default',
#                                     badge=1, extra=text)
#                 resu = "sent"
#             except:
#                 resu = "failed"
#     return resu


def isNtEmt(s):
    return bool(s and s.strip())


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        print(self.request)
        return data.encode(self.charset)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # check that a ValidationError exception is raised
    if isinstance(exc, ValidationError):
        # here prepare the 'custom_error_response' and
        # set the custom response data on response objec
        result = []

        response = exception_handler(exc, context)
        exc2 = exc.__dict__['detail']

        try:
            # for field, msg in exc2.items():
            for k in list(exc2.keys()):
                # print(msg)
                field = k
                msg = exc2[k]

                for i in range(len(msg)):
                    message_ = str(msg[i])
                    message_ = message_.replace("This field", str(field).title())
                    result.append(message_)

                # message_ = str(msg[0])
                response.data['errors'] = result
        except AttributeError:
            # result.append(exc2)
            # print(exc.__dict__['detail'])
            data = {
                'data': response.data,
                'errors': exc2
            }
            response.data = data

    return response
