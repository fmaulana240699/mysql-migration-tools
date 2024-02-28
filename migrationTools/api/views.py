from .models import migrationData, repoIntegration, migrationConfig
from .serializers import migrationDataSerializer, repoIntegrationSerializer, migrationConfigSerializer
from .github_helper import githubHelper
from .tasks import execute_remote_query
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

class migrationHistoryAPIView(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    queryset = migrationData.objects.all()
    serializer_class = migrationDataSerializer
    

class migrationConfigCreateListAPIView(generics.ListCreateAPIView):
    queryset = migrationConfig.objects.all()
    serializer_class = migrationConfigSerializer

class WebhookAPIView(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]

    queryset = migrationData.objects.all()
    serializer_class = migrationDataSerializer

    def get(self, request):
        not_yet = []
        try:
            last_migrate = self.queryset.filter(id_repo=1)
            dict = self.serializer_class(last_migrate, many=True)
            gh = githubHelper("fmaulana240699/mysql-migration-tools", "migrations-data")
            list_file = gh.get_list_file()
            for x in list_file:
                for y in dict.data:
                    if x in y["file_name"]:
                        # print("done")
                        pass
                    else:
                        # print("belum")  
                        not_yet.append(x)
            
            test = list(set(not_yet))
            query = []
            for z in test:
                # print(z)
                query.append(gh.get_migration(z))
            
            # put on celery to for the query to be executed
            for p in query:
                execute_remote_query.delay(p)

        except Exception as e:
            print("a")
            print(e)
            return Response("test", status=400) 
        
        return Response("good", status=200)
        
       

