from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import Sneaker

# class Sneaker:
#   def __init__(self, name, brand, date, description, price):
#     self.name = name
#     self.brand = brand
#     self.date = date
#     self.description = description
#     self.price = price

# sneakers = [
#   Sneaker('Air Jordan 1 High "Bleached Coral"', 'Nike', 'July 2, 2022', 'Black/White/Amethyst Wave/Bleached Coral', 170),
#   Sneaker('Nike Air Bo Turf "White And Solar Red"', 'Nike', 'July 6, 2022', 'White/Solar Red-Black', 140),
#   Sneaker('Martine Rose X Nike MR4 Shox "Black"', 'Nike', 'July 7, 2022', 'BLACK/METALLIC SILVER-COMET', 180)
# ]

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def sneakers_index(request):
  sneakers = Sneaker.objects.all().order_by('date')
  return render(request, 'sneakers/index.html', { 'sneakers': sneakers })

def sneakers_detail(request, sneaker_id):
    sneaker = Sneaker.objects.get(id=sneaker_id)
    return render(request, 'sneakers/detail.html', {'sneaker': sneaker})

class SneakerCreate(CreateView):
  model = Sneaker
  fields = '__all__'

class SneakerUpdate(UpdateView):
    model = Sneaker
    fields = ['brand', 'date', 'description', 'price']

class SneakerDelete(DeleteView):
  model = Sneaker
  success_url = '/sneakers/'