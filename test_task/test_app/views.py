from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView

from .backends import JWTAuthentication
from .models import User, Organization, Event
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, OrganizationSerializer, EventSerializer
)


class RegistrationAPIView(APIView):
    renderer_classes = (UserJSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



class EventCreateView(APIView):
    """Создание мероприятия"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OrganizationCreateView(APIView):
    """Создание организации"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class OrganizationView(APIView):
    """Получение списка организаций"""
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        """
        :return: фильтрованный queryset организаций
        :rtype:  QuerySet
        """
        queryset = Organization.objects.all()
        return queryset

    def get(self, request):
        return self.list(request)


class EventView(ListModelMixin, GenericAPIView):
    """Получение списка мероприятий"""
    serializer_class = EventSerializer

    def get_queryset(self):
        """
        :return: фильтрованный queryset мероприятий
        :rtype:  QuerySet
        """
        queryset = Event.objects.all()

        # Фильтрация по дате
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if date_from and date_to:
            queryset = queryset.filter(date__range=[date_from, date_to])

        # Сортировка по дате
        sort_by_date = self.request.query_params.get('sort_by_date', None)
        if sort_by_date == 'asc':
            queryset = queryset.order_by('date')
        elif sort_by_date == 'desc':
            queryset = queryset.order_by('-date')

        # Поиск по названию
        search_query = self.request.query_params.get('search_query', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        # Лимитная пагинация
        limit = self.request.query_params.get('limit', None)
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass

        return queryset

    def get(self, request):
        return self.list(request)

