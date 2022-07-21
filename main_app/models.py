from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta, date

PLACES = (
        ('P', 'Play'),
        ('W', 'Work'),
        ('S', 'School'),
        ('C', 'Chill'),
        ('A', 'Athletics')
    )

class Protector(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('protectors_detail', kwargs={'pk': self.id})

class Sneaker(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    date = models.DateField('release date')
    price = models.IntegerField()
    protectors = models.ManyToManyField(Protector)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={ 'sneaker_id': self.id })

    def worn_today(self):
        today = datetime.now()
        one_month_ago = today - timedelta(days=31)
        # time_range = DateTimeRange(today(), one_month_ago)
        return self.worn_set.filter(date=date.today())
        # return self.worn_set.filter(date_list=today - one_month_ago)
        # print(self.worn_set.filter(date=today - one_month_ago))
        # print(self.worn_set.filter(date=date).count())
        
class Worn(models.Model):
    date = models.DateField('date worn')
    place = models.CharField(
        max_length=1,
        choices=PLACES,
        default=PLACES[0][0]
    )
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_place_display()} on {self.date}"

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for sneaker_id: {self.sneaker_id} @{self.url}"