from django.urls import path
from account.views import (
    profil_view,
)
app_name = "account"

urlpatterns = [
    path('<user_id>/', profil_view, name='profile'),
]
