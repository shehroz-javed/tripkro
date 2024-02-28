from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from account.serializers import UserRegisterSerializer


class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "User registered successfully", "payload": serializer.data},
                status=status.HTTP_201_CREATED,
            )
