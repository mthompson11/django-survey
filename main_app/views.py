from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Survey, Question
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, SurveyCreateForm, QuestionCreateForm, QuestionEditForm
import boto3
import os
import uuid

def home(request):
  return render(request,'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('login')
    else:
      error_message = 'Invalid sign up - try again'
  form = CustomUserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def create_survey(request):
  error_message = ''
  if request.method == 'POST':
    photo_file = request.FILES.get('photo-file', None)
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
        bucket = os.environ['S3_BUCKET']
        s3.upload_fileobj(photo_file, bucket, key)
        url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
        data = {
          'name': request.POST['name'],
          'description': request.POST['description'],
          'imageURL': url,
          'owner': request.user,
          'status' : 'D'
        }
        form = SurveyCreateForm(data)
        if form.is_valid():
          survey = form.save()
          return redirect('question_create', survey_id=survey.id)
        else:
          error_message = 'Invalid survey - try again'
    except Exception as e:
      error_message = 'An error occurred uploading file to S3'
  context = {'error_message': error_message}
  return render(request, 'surveys/create.html', context)

@login_required
def surveys_index(request):
  surveys = Survey.objects.all()
  for survey in surveys:
    if Question.objects.filter(survey=survey).exists():
      survey.hasQuestions = True
    if survey.users_taken.filter(id=request.user.id).exists():
      survey.taken = True
    else:
      survey.taken = False
  return render(request, 'surveys/index.html', {'surveys' : surveys})

class surveys_create(LoginRequiredMixin, CreateView):
  model = Survey
  form_class = SurveyCreateForm
  
  def form_valid(self, form):
    form.instance.owner = self.request.user
    return super().form_valid(form)


class questions_create(LoginRequiredMixin, CreateView):
  model = Question
  form_class = QuestionCreateForm

  def form_valid(self, form):
    print(self.kwargs['survey_id'])
    form.instance.survey = Survey.objects.get(id=self.kwargs['survey_id'])
    return super().form_valid(form)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['survey'] = Survey.objects.get(id=self.kwargs['survey_id'])
    context['questions'] = Question.objects.filter(survey=self.kwargs['survey_id'])
    return context

@login_required
def survey_detail(request, survey_id):
  survey = Survey.objects.get(id=survey_id)
  questions = Question.objects.filter(survey=survey_id)
  taken = survey.users_taken.filter(id=request.user.id).exists()
  taken_count = len(survey.users_taken.all())
  return render(request, 'surveys/detail.html', {'survey': survey, 'questions': questions, 'taken': taken, 'taken_count' : taken_count})

@login_required
def dashboard(request):
  surveys = Survey.objects.filter(owner=request.user.id)
  for survey in surveys:
    if survey.users_taken.filter(id=request.user.id).exists():
      survey.taken = True
    else:
      survey.taken = False
  surveys = {
    'draft' : surveys.filter(status='D'),
    'published' : surveys.filter(status='P'),
    'closed' : surveys.filter(status='C')
  }
  return render(request, 'dashboard.html', {'surveys' : surveys})

class SurveyDelete(LoginRequiredMixin, DeleteView):
  model = Survey
  success_url = '/dashboard/'

@login_required
def survey_vote(request, survey_id):
  for key, value in request.POST.items():
    if key != 'csrfmiddlewaretoken':
      q = Question.objects.get(id=key)
      votes = getattr(q, f"{value}_votes")
      setattr(q, f"{value}_votes", votes + 1)
      q.save()
  return redirect('assoc_user', survey_id=survey_id, user_id=request.user.id)

@login_required
def survey_answer(request, survey_id):
  survey = Survey.objects.get(id=survey_id)
  questions = Question.objects.filter(survey=survey_id)
  return render(request, 'surveys/answer.html', {'survey': survey, 'questions': questions})

@login_required
def assoc_user(request, survey_id, user_id):
  Survey.objects.get(id=survey_id).users_taken.add(user_id)
  return redirect('index')

@login_required
def update_status(request, survey_id, status):
  questions = Question.objects.filter(survey=survey_id)
  if status == 'P' and len(questions) != 0:
    Survey.objects.filter(id=survey_id).update(status=status)
  elif status == 'C':
    Survey.objects.filter(id=survey_id).update(status=status)
  return redirect('detail', survey_id=survey_id)

@login_required
def edit(request, survey_id):
  survey = Survey.objects.get(id=survey_id)
  questions = Question.objects.filter(survey=survey_id)
  return render(request, 'edit.html', {'survey': survey, 'questions': questions})

class question_edit(LoginRequiredMixin, UpdateView):
  model = Question
  template_name = 'question_edit.html'
  form_class = QuestionEditForm

  