from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sneaker, Protector, Photo
from .forms import WornForm
import uuid
import boto3

S3_BASE_URL='https://s3-us-west-1.amazonaws.com/'
BUCKET='sneakerhead-ar-83'

class SneakerCreate(LoginRequiredMixin, CreateView):
  model = Sneaker
  fields = ['name','brand', 'date', 'description', 'price']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class SneakerUpdate(LoginRequiredMixin, UpdateView):
    model = Sneaker
    fields = ['brand', 'date', 'description', 'price']

class SneakerDelete(LoginRequiredMixin, DeleteView):
  model = Sneaker
  success_url = '/sneakers/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def sneakers_index(request):
  sneakers = Sneaker.objects.filter(user=request.user)
  return render(request, 'sneakers/index.html', { 'sneakers': sneakers })

@login_required
def sneakers_detail(request, sneaker_id):
  sneaker = Sneaker.objects.get(id=sneaker_id)
  protectors_sneaker_doesnt_have = Protector.objects.exclude(id__in = sneaker.protectors.all().values_list('id'))
  worn_form = WornForm()
  return render(request, 'sneakers/detail.html', {
    'sneaker': sneaker, 'worn_form': worn_form,
    'protectors': protectors_sneaker_doesnt_have,
  })

@login_required
def add_worn(request, sneaker_id):
  form = WornForm(request.POST)
  if form.is_valid():
    new_worn = form.save(commit=False)
    new_worn.sneaker_id = sneaker_id
    new_worn.save()
  return redirect('detail', sneaker_id=sneaker_id)

@login_required
def add_photo(request, sneaker_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, sneaker_id=sneaker_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', sneaker_id=sneaker_id)

@login_required
def assoc_protector(request, sneaker_id, protector_id):
  Sneaker.objects.get(id=sneaker_id).protectors.add(protector_id)
  return redirect('detail', sneaker_id=sneaker_id)

class ProtectorList(LoginRequiredMixin, ListView):
  model = Protector

class ProtectorDetail(LoginRequiredMixin, DetailView):
  model = Protector

class ProtectorCreate(LoginRequiredMixin, CreateView):
  model = Protector
  fields = '__all__'

class ProtectorUpdate(LoginRequiredMixin, UpdateView):
  model = Protector
  fields = ['name', 'color']

class ProtectorDelete(LoginRequiredMixin, DeleteView):
  model = Protector
  success_url = '/Protector/'