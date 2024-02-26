from .models import migrationData, repoIntegration
from .serializers import migrationDataSerializer, repoIntegrationSerializer
from .github_helper import githubHelper
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken, RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.forms.models import model_to_dict
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.serializers import serialize
import json

class repoCreateListAPIView(generics.ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    queryset = repoIntegration.objects.all()
    serializer_class = repoIntegrationSerializer 

class migrationCreateListAPIView(generics.ListCreateAPIView):
    queryset = migrationData.objects.all()
    serializer_class = migrationDataSerializer 
    def get(self, request):
        data_git = githubHelper("fmaulana240699/mysql-migration-tools", "test.sql", "migrations-data/")
        test = data_git.get_migration()
        test2 = data_git.get_last_commit_author()
        data=test+test2
        return Response(data, status=200)
    
    def post(self, request):
        data_git = githubHelper("fmaulana240699/mysql-migration-tools", request.data["file_name"], "migrations-data/")
        data = request.data
        try:
            get_data = migrationData.objects.all()
            filter = get_data.filter(id_repo=1).latest("created_at")
            batch=filter.batch_version+1
        except:
            batch=1

        serializer = migrationDataSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data["sql_query"] = data_git.get_migration()
            serializer.validated_data["author"] = data_git.get_last_commit_author()
            serializer.validated_data["batch_version"] = batch
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)     

class WebhookAPIView(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]

    queryset = migrationData.objects.all()
    serializer_class = migrationDataSerializer

    def get(self, request):
        not_yet = []
        try:
            last_migrate = self.queryset.filter(id_repo=1)
            dict = self.serializer_class(last_migrate, many=True)
            
            gh = githubHelper("fmaulana240699/mysql-migration-tools", "test.sql", "migrations-data/")
            list_file = ['nyobain.sql', 'testing.sql'] #gh.compare_migration()
            for x in list_file:
                for y in dict.data:
                    if x in y["file_name"]:
                        print("done")
                    else:
                        print("belum")  
                        not_yet.append(x)
            print(set(not_yet))
            
            # put on celery to for the query to be executed

        except:
            return Response("test", status=400) 
        
        return Response("error", status=200)
        
       

