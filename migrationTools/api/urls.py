from django.urls import path
from .views import repoCreateListAPIView, migrationHistoryAPIView, WebhookAPIView, migrationConfigCreateListAPIView

urlpatterns = [
    path('repo/', repoCreateListAPIView.as_view(), name='list-create-repo'),
    path('migration/', migrationHistoryAPIView.as_view(), name='list-migration-history'),
    path('migration/config', migrationConfigCreateListAPIView.as_view(), name='create-migration-config'),
    path('webhook/', WebhookAPIView.as_view(), name='webhook-trigger-migration')
    # path('barang/delete/', BarangDeleteView.as_view(), name='barang-delete'),
    # path('barang/<int:pk>/', BarangUpdateView.as_view(), name='barang-update'),
    
]
