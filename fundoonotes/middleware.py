from rest_framework import status
from rest_framework.response import Response


class NoteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def process_exception(self, request, exception):
        # print(request.data)
        return Response({'message': "Coming from middleware " + str(exception)}, status=status.HTTP_404_NOT_FOUND)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response