from django.urls import path
from . import views
from main_app.forms import CustomAuthenticationForm
from django.contrib.auth import views as django_views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/',
        django_views.LoginView.as_view(template_name="registration/login.html",
                                        authentication_form=CustomAuthenticationForm),
        name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('surveys/<int:survey_id>/', views.survey_detail, name='detail'),
    path('surveys/', views.surveys_index, name='index'),
    path('surveys/create', views.create_survey, name='create'),
    #path('surveys/create', views.surveys_create.as_view(), name='create'),
    #path('survey/<int:survey_id>/questions/create', views.create_question, name='question_create'),
    path('survey/<int:survey_id>/questions/create', views.questions_create.as_view(), name='question_create'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('surveys/<int:pk>/delete/', views.SurveyDelete.as_view(), name='survey_delete'),
    path('survey/<int:survey_id>/vote/', views.survey_vote, name='survey_vote'),
    path('survey/<int:survey_id>/answer', views.survey_answer, name='survey_answer'),
    path('survey/<int:survey_id>/assoc_user/<int:user_id>/', views.assoc_user, name = 'assoc_user')
]