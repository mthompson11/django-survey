from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Survey, Question
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('login')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def home(request):
  return redirect('login')

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
  fields = ['name', 'description']

  def form_valid(self, form):
    form.instance.owner = self.request.user
    return super().form_valid(form)


class questions_create(LoginRequiredMixin, CreateView):
  model = Question
  fields = ['question_text', 'option_one', 'option_two', 'option_three']

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
    if Question.objects.filter(survey=survey).exists():
      survey.hasQuestions = True
    else:
      survey.hasQuestions = False
    if survey.users_taken.filter(id=request.user.id).exists():
      survey.taken = True
    else:
      survey.taken = False
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


  