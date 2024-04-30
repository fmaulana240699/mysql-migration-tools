from django.urls import path
from .views import repoCreateListAPIView, WebhookAPIView, migrationConfigCreateListAPIView, MigrationHistoryListView, RepoDeleteView, RepoUpdateView, MigrationConfigDeleteView, MigrationConfigUpdateView, RegisterView, LoginView, LogoutView, UserDeleteView, UserUpdateView, UserListView, MigrationHistoryListDetailsView

urlpatterns = [
    path('repo/', repoCreateListAPIView.as_view(), name='list-create-repo'),
    path('repo/delete/', RepoDeleteView.as_view(), name='repo-delete'),
    path('repo/<int:pk>/', RepoUpdateView.as_view(), name='repo-update'),
    path('migration/', MigrationHistoryListView.as_view(), name='list-migration-history'),
    path('migration/<str:identifier>', MigrationHistoryListDetailsView.as_view(), name='list-migration-history-details'),
    path('migration/config/', migrationConfigCreateListAPIView.as_view(), name='create-migration-config'),
    path('migration/config/delete/', MigrationConfigDeleteView.as_view(), name='migration-config-delete'),
    path('migration/config/<int:pk>/', MigrationConfigUpdateView.as_view(), name='migration-config-update'),   
    path('webhook/<str:identifier>', WebhookAPIView.as_view(), name='webhook-trigger-migration'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user-details-update'),
    path('users/delete/', UserDeleteView.as_view(), name='user-delete'),
    
]
