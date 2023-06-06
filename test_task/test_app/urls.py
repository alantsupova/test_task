from django.urls import path

from .views import OrganizationCreateView,EventCreateView, OrganizationView, EventView, RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView


urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('organization/', OrganizationView.as_view()),
    path('event/', EventView.as_view()),
    path('event/create/', EventCreateView.as_view(), name='event_create'),
    path('organization/create/', OrganizationCreateView.as_view(), name='organization_create'),
]
