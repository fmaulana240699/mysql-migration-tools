from django.urls import path
from .views import repoCreateListAPIView, migrationCreateListAPIView

urlpatterns = [
    path('repo/', repoCreateListAPIView.as_view(), name='list-create-repo'),
    path('migration/', migrationCreateListAPIView.as_view(), name='list-create-migration'),
    # path('barang/delete/', BarangDeleteView.as_view(), name='barang-delete'),
    # path('barang/<int:pk>/', BarangUpdateView.as_view(), name='barang-update'),
    
]
