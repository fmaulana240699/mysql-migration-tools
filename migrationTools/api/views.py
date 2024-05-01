from .models import migrationData, repoIntegration, migrationConfig, Users
from .serializers import migrationDataSerializer, repoIntegrationSerializer, migrationConfigSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .github_helper import githubHelper
import re
from rest_framework.response import Response
from django.template.loader import get_template
from .tasks import execute_remote_query
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .custom_permissions import IsAdmin, IsViewer
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from django.core.serializers import serialize

class repoCreateListAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]  
    queryset = repoIntegration.objects.all()
    serializer_class = repoIntegrationSerializer  

class RepoDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]  

    def delete(self, request):
        repo_id = request.data.get('id')

        try:
            repo = repoIntegration.objects.get(id=repo_id)
            repo.delete()
            return Response({'message': 'Repository berhasil dihapus'}, status=204)
        except repoIntegration.DoesNotExist:
            return Response({'message': 'Repository tidak ditemukan'}, status=404)    
        
class RepoUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]  

    def get(self, request, pk):
        try:
            repo = repoIntegration.objects.get(pk=pk)
            repo = model_to_dict(repo)
            return Response(repo, status=200)
        except repoIntegration.DoesNotExist:
            return Response({'message': 'Repository tidak ditemukan'}, status=404)   

    def patch(self, request, pk):
        try:
            repo = repoIntegration.objects.get(pk=pk)
            serializer = repoIntegrationSerializer(repo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except repoIntegration.DoesNotExist:
            return Response({'message': 'Repository tidak ditemukan'}, status=404)        

class migrationConfigCreateListAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]      
    queryset = migrationConfig.objects.all()
    serializer_class = migrationConfigSerializer

class MigrationConfigDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]  

    def delete(self, request):
        migration_id = request.data.get('id')

        try:
            migration = migrationConfig.objects.get(id=migration_id)
            migration.delete()
            return Response({'message': 'Migration Config berhasil dihapus'}, status=204)
        except migrationConfig.DoesNotExist:
            return Response({'message': 'Migration Config tidak ditemukan'}, status=404)

class MigrationConfigUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]

    def get(self, request, pk):
        try:
            migration = migrationConfig.objects.get(pk=pk)
            migration = model_to_dict(migration)
            return Response(migration, status=200)
        except migrationConfig.DoesNotExist:
            return Response({'message': 'Migration tidak ditemukan'}, status=404)     

    def patch(self, request, pk):
        try:
            migration = migrationConfig.objects.get(pk=pk)
            serializer = migrationConfigSerializer(migration, data=request.data, partial=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                if validated_data.get("db_password"):
                    validated_data["db_password"] = make_password(request.data["db_password"])
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except migrationConfig.DoesNotExist:
            return Response({'message': 'Migration config tidak ditemukan'}, status=404)        


class WebhookAPIView(generics.ListAPIView):
    queryset = migrationData.objects.all()
    serializer_class = migrationDataSerializer
    not_yet = []

    def filter_file_name(self, string):
        # match = re.search(r'/([^/]+)$', string)
        # return match.group(0)
        match = re.search(r'[^/]+$', string)
        return match.group(0)        


    def get(self, request, identifier):
        
        ### compare last migration ###
        last_migrate = self.queryset.filter(id_repo=identifier)
        dict = self.serializer_class(last_migrate, many=True)
        migration = migrationConfig.objects.get(id_repo=identifier)
        repo = repoIntegration.objects.get(pk=identifier)
        repo.decrypt()
        gh = githubHelper(repo.repo_url, migration.folder_location, repo.token)
        list_file = gh.get_list_file()
        author = gh.get_last_commit_author()

        for file_name in list_file:
            found = False
            for item in dict.data:
                if file_name in item["file_name"]:
                    found = True
                    pass
            if not found:
                self.not_yet.append(file_name)        
        print(len(self.not_yet))    
        test = list(set(self.not_yet))

        if len(test) != 0: 
            try:
                query = []
                for z in test:
                    query.append({"query": gh.get_migration(z), "file_loc": z})
                
                repo_integration_instance = repoIntegration.objects.get(pk=identifier)

                # put on celery to for the query to be executed
                for p in query:
                    history_id = migrationData.objects.create(sql_query=p["query"], status_query="in queue", db_name=migration.db_name, engineer_name=author, error_log=None, file_name=str(self.filter_file_name(p["file_loc"])), id_repo=repo_integration_instance)
                    execute_remote_query.delay(p["query"], identifier, history_id.id, "/" + str(self.filter_file_name(p["file_loc"])))
                
                test.clear()
                self.not_yet.clear()
            except Exception as e:
                print(e)
                return Response("error", status=400)
        else:
            print("skip gan")
        
        return Response("successfully in queue", status=200)
        
       
class HistoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

class MigrationHistoryListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & (IsAdmin | IsViewer)]  
    pagination_class = HistoryPagination

    def get(self, request):
        items = migrationData.objects.all()
        paginator = HistoryPagination()
        result_page = paginator.paginate_queryset(items, request)
        for item in result_page:
            item.created_at = item.created_at.strftime("%Y-%m-%d %H:%M")
            item.updated_at = item.updated_at.strftime("%Y-%m-%d %H:%M")

        serializer = migrationDataSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class MigrationHistoryListDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & (IsAdmin | IsViewer)]  

    def get(self, request, identifier):

        try: 
            data = migrationData.objects.filter(id=identifier).first()

            return Response({
                "id": data.id, 
                "sql_query": data.sql_query
            }, status=200)
        except Exception as e:
            return Response(status=404)   
    
class RegisterView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = Users.objects.filter(username=username).first()

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                "id": user.id,
                "role": user.role
                # "fullname": user.fullname
            }
        })

class LogoutView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & (IsAdmin | IsViewer)]  

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=205)
        except Exception as e:
            return Response(status=400)       
        

class UserDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]

    def delete(self, request):
        user_id = request.data.get('id')
        print(user_id)
        try:
            user = Users.objects.get(id=user_id)
            user.delete()
            return Response({'message': 'User berhasil dihapus'}, status=204)
        except Users.DoesNotExist:
            return Response({'message': 'User tidak ditemukan'}, status=404)

class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]

    def get(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            user = model_to_dict(user)
            return Response(user, status=200)
        except Users.DoesNotExist:
            return Response({'message': 'User tidak ditemukan'}, status=404)     

    def patch(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                if validated_data.get("password"):
                    validated_data["password"] = make_password(request.data["password"])
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Users.DoesNotExist:
            return Response({'message': 'User tidak ditemukan'}, status=404) 
        
class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]      
    queryset = Users.objects.all()
    serializer_class = UserSerializer