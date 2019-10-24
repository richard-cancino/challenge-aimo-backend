from rest_framework import generics, status, filters
from django.db import transaction
from django.contrib.auth import user_logged_in
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from account.api.serializers import CreateNoteSerializer, \
    RetrieveNoteSerializer, LoginSerializer, CreateUserSerializer
from account.models import Note
from django.utils.decorators import method_decorator
from rest_framework_jwt.serializers import jwt_payload_handler, \
    jwt_encode_handler


class CreateUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

    @method_decorator(transaction.atomic)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateUserAPIView, self).dispatch(request, *args,
                                                       **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        payload = jwt_payload_handler(user)
        return Response({'token': jwt_encode_handler(payload)})


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_logged_in.send(
            sender=serializer.validated_data.get("user").__class__,
            request=request,
            user=serializer.validated_data.get("user"))
        response_data = {"token": serializer.validated_data.get('token')}
        return Response(response_data)


class NoteAPIView(generics.ListCreateAPIView):
    serializer_class = CreateNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Note.objects.filter(is_active=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RetrieveNoteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RetrieveNoteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = self.perform_create(serializer)
        if note:
            serializer = CreateNoteSerializer(note, context={
                'request': request})
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return Response(
                {'details': [{
                    'object': 'Error',
                    'code': 'E00-001'}]},
                status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save()
