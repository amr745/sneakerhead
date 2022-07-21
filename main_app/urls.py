from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sneakers/', views.sneakers_index, name='index'),
    path('sneakers/<int:sneaker_id>/', views.sneakers_detail, name='detail'),
    path('sneakers/create/', views.SneakerCreate.as_view(), name='sneakers_create'),
    path('sneakers/<int:pk>/update/', views.SneakerUpdate.as_view(), name='sneakers_update'),
    path('sneakers/<int:pk>/delete/', views.SneakerDelete.as_view(), name='sneakers_delete'),
    path('sneakers/<int:sneaker_id>/add_worn/', views.add_worn, name='add_worn'),
    path('sneakers/<int:sneaker_id>/add_photo/', views.add_photo, name='add_photo'),
    path('sneakers/<int:sneaker_id>/assoc_protector/<int:protector_id>/', views.assoc_protector, name='assoc_protector'),
    path('protectors/', views.ProtectorList.as_view(), name='protectors_index'),
    path('protectors/<int:pk>/', views.ProtectorDetail.as_view(), name='protectors_detail'),
    path('protectors/create/', views.ProtectorCreate.as_view(), name='protectors_create'),
    path('protectors/<int:pk>/update/', views.ProtectorUpdate.as_view(), name='protectors_update'),
    path('protectors/<int:pk>/delete/', views.ProtectorDelete.as_view(), name='protectors_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]