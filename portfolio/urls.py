from django.urls import path

from . import views

urlpatterns = [
	path('', views.main_view, name="main"),
	path('add_stock/', views.add_stock_view, name="add_stock"),
	path('delete/<id>', views.delete_stock_view, name="delete"),
	path('<id>/update', views.update_view, name="update"),
]
