from django.shortcuts import render
from django.http import HttpResponse

class Sneaker:
  def __init__(self, name, release, description, price):
    self.name = name
    self.release = release
    self.description = description
    self.price = price

sneakers = [
  Sneaker('Air Jordan 1 High "Bleached Coral"', 'July 2, 2022', 'Black/White/Amethyst Wave/Bleached Coral', 170),
  Sneaker('Nike Air Bo Turf "White And Solar Red"', 'July 6, 2022', 'White/Solar Red-Black', 140),
  Sneaker('Martine Rose X Nike MR4 Shox "Black"', 'July 7, 2022', 'BLACK/METALLIC SILVER-COMET', 180)
]

# Define the home view
def home(request):
  return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def about(request):
  return render(request, 'about.html')

def sneakers_index(request):
  return render(request, 'sneakers/index.html', { 'sneakers': sneakers })