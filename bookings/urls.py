from django.urls import path
from .views import RegisterView, LoginView, BusListCreateView, BusDetailView, BookingView , UserBookingsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('buses/', BusListCreateView.as_view(), name='bus-list-create'),
    path('bookings/', BookingView.as_view(), name='booking'),
    path('user-bookings/', UserBookingsView.as_view(), name='user-bookings'),
]