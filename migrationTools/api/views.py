from .models import migrationData, repoIntegration, migrationConfig
from .serializers import migrationDataSerializer, repoIntegrationSerializer, migrationConfigSerializer
from .github_helper import githubHelper
import re
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
    not_yet = []

    def filter_file_name(self, string):
        pattern = r'\d{4}-\d{2}-\d{2}-\d{3}'
        print(string)
        match = re.search(pattern, string)
        print(match)
        return match

    def get(self, request):
        
        ### compare last migration ###
        last_migrate = self.queryset.filter(id_repo=request.data["id_repo"])
        dict = self.serializer_class(last_migrate, many=True)
        gh = githubHelper("fmaulana240699/mysql-migration-tools", "migrations-data")
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
                
                repo_integration_instance = repoIntegration.objects.get(pk=request.data["id_repo"])

                # put on celery to for the query to be executed
                for p in query:
                    history_id = migrationData.objects.create(sql_query=p["query"], status_query="in queue", author=author, error_log=None, file_name=p["file_loc"], id_repo=repo_integration_instance)
                    execute_remote_query.delay(p["query"], request.data["id_repo"], history_id.id, self.filter_file_name(p["file_loc"]))
                
                test.clear()
                self.not_yet.clear()
            except Exception as e:
                print(e)
                return Response("error", status=400)
        else:
            print("skip gan")
        
        return Response("good", status=200)
        
       

