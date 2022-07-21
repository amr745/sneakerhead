from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Sneaker, Protector, Photo
from .forms import WornForm

import uuid
import boto3

S3_BASE_URL='https://s3-us-west-1.amazonaws.com/'
BUCKET='sneakerhead-ar-83'

class SneakerCreate(CreateView):
  model = Sneaker
  fields = ['name','brand', 'date', 'description', 'price']

class SneakerUpdate(UpdateView):
    model = Sneaker
    fields = ['brand', 'date', 'description', 'price']

class SneakerDelete(DeleteView):
  model = Sneaker
  success_url = '/sneakers/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def sneakers_index(request):
  sneakers = Sneaker.objects.all().order_by('date')
  return render(request, 'sneakers/index.html', { 'sneakers': sneakers })

def sneakers_detail(request, sneaker_id):
  sneaker = Sneaker.objects.get(id=sneaker_id)
  protectors_sneaker_doesnt_have = Protector.objects.exclude(id__in = sneaker.protectors.all().values_list('id'))
  worn_form = WornForm()
  return render(request, 'sneakers/detail.html', {
    'sneaker': sneaker, 'worn_form': worn_form,
    'protectors': protectors_sneaker_doesnt_have,
  })

def add_worn(request, sneaker_id):
  form = WornForm(request.POST)
  if form.is_valid():
    new_worn = form.save(commit=False)
    new_worn.sneaker_id = sneaker_id
    new_worn.save()
  return redirect('detail', sneaker_id=sneaker_id)

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

def assoc_protector(request, sneaker_id, protector_id):
  Sneaker.objects.get(id=sneaker_id).protectors.add(protector_id)
  return redirect('detail', sneaker_id=sneaker_id)

class ProtectorList(ListView):
  model = Protector

class ProtectorDetail(DetailView):
  model = Protector

class ProtectorCreate(CreateView):
  model = Protector
  fields = '__all__'

class ProtectorUpdate(UpdateView):
  model = Protector
  fields = ['name', 'color']

class ProtectorDelete(DeleteView):
  model = Protector
  success_url = '/Protector/'