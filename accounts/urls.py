from django.urls import path
from .views import save_dynamic_form , list_saved_forms, use_form
from . import views 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('create-dynamic-form/', views.create_dynamic_form_view, name='create_dynamic_form'),  # Dynamic form design
    path('save-dynamic-form/', save_dynamic_form, name='save_dynamic_form'),
    path('saved-forms/', list_saved_forms, name='list_saved_forms'),
    path('use-form/<int:form_id>/', use_form, name='use_form')
]
