from .models import migrationData, repoIntegration, migrationConfig, Users
from .serializers import migrationDataSerializer, repoIntegrationSerializer, migrationConfigSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .github_helper import githubHelper, ConnectionTesting
from .mysql_helper import MysqlConnection
import re
import json
import os
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
from xhtml2pdf import pisa
from io import BytesIO
from datetime import timedelta
from django.utils import timezone
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'migrationTools.settings')
app = Celery('migrationTools')
app.config_from_object('django.conf:settings', namespace='CELERY')

class repoCreateListAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]
    queryset = repoIntegration.objects.all()
    serializer_class = repoIntegrationSerializer

    def post(self, request):
        data = request.data
        gh = ConnectionTesting(data["repo_url"], data["token"])
        if gh.check():
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Repository successfully created'}, status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'message': 'Github connection problem'}, status=500)

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

    def get(self, request, identifier):
        try:
            repo = repoIntegration.objects.get(id=identifier)
            repo = model_to_dict(repo)
            return Response(repo, status=200)
        except repoIntegration.DoesNotExist:
            return Response({'message': 'Repository tidak ditemukan'}, status=404)

    def patch(self, request, identifier):
        try:
            repo = repoIntegration.objects.get(id=identifier)
            print(request.data)
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

    def post(self, request):
        data = request.data
        check = MysqlConnection(data["db_host"],data["db_user"],data["db_password"],data["db_name"])

        if check.testing_connection():
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'message': 'Database connection problem'}, status=500)

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

    def get(self, request, identifier):
        try:
            migration = migrationConfig.objects.get(id=identifier)
            migration = model_to_dict(migration)
            return Response(migration, status=200)
        except migrationConfig.DoesNotExist:
            return Response({'message': 'Migration tidak ditemukan'}, status=404)

    def patch(self, request, identifier):
        try:
            migration = migrationConfig.objects.get(id=identifier)
            serializer = migrationConfigSerializer(migration, data=request.data, partial=True)
            if serializer.is_valid():
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
        if string.endswith('/'):
            return string.rstrip('/').split('/')[-1]
        return string.split('/')[-1]

    def filter_batch(self, string):
        pattern = r"(\d{14})"
        match = re.search(pattern, string)

        if match:
            return match.group(1)
        return None

    def get_celery_worker_status(self):
        try:
            inspector = app.control.inspect()
            active_workers = inspector.active()
            if not active_workers:
                print('No active workers found.')
                return False
            return True
        except Exception as e:
            print(f"Error : {e}")
            return False



    def post(self, request, identifier):

        ### compare last migration ###
        last_migrate = self.queryset.filter(id_repo=identifier)
        dict = self.serializer_class(last_migrate, many=True)
        migration = migrationConfig.objects.get(id_repo=identifier)
        repo = repoIntegration.objects.get(pk=identifier)
        repo.decrypt()
        gh = githubHelper(repo.repo_url, migration.folder_location, repo.branch, repo.token)
        list_file = gh.get_list_file()
        author = gh.get_last_commit_author()

        for file_name in list_file:
            found = False
            for item in dict.data:
                if  item["file_name"] in file_name:
                    found = True
                    print("udah pernah run")
                    pass
            if not found:
                self.not_yet.append(file_name)
                print("ga nemu")
        test = list(set(self.not_yet))

        if len(test) != 0:
            try:
                query = []
                for z in test:
                    query.append({"query": gh.get_migration(z), "file_loc": z})

                repo_integration_instance = repoIntegration.objects.get(pk=identifier)

                #check worker
                check_worker = True #self.get_celery_worker_status()
                if check_worker:
                    # put on celery to for the query to be executed
                    for p in query:
                        history_id = migrationData.objects.create(sql_query=p["query"], status_query="in queue", db_name=migration.db_name, engineer_name=author, error_log=None, file_name=str(self.filter_file_name(p["file_loc"])), id_repo=repo_integration_instance)
                        execute_remote_query.delay(p["query"], identifier, history_id.id, str(self.filter_batch(p["file_loc"])))

                    test.clear()
                    self.not_yet.clear()
                else:
                    for p in query:
                        history_id = migrationData.objects.create(sql_query=p["query"], status_query="Error", db_name=migration.db_name, engineer_name=author, error_log="No Worker Found", file_name=str(self.filter_file_name(p["file_loc"])), id_repo=repo_integration_instance)
                    return Response("No Worker Found", status=500)
            except Exception as e:
                print(e)
                return Response("error", status=400)
        else:
            print("skip gan")

        return Response("successfully in queue", status=200)


class HistoryPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class MigrationHistoryListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & (IsAdmin | IsViewer)]
    pagination_class = HistoryPagination

    def get(self, request):
        items = migrationData.objects.all()
        paginator = HistoryPagination()
        result_page = paginator.paginate_queryset(items, request, view=self)
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
                "username": user.username,
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
            user = Users.objects.get(id=pk)
            user = model_to_dict(user)
            return Response(user, status=200)
        except Users.DoesNotExist:
            return Response({'message': 'User tidak ditemukan'}, status=404)

    def patch(self, request, pk):
        try:
            user = Users.objects.get(id=pk)
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

class ExportHistory(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & (IsAdmin | IsViewer)]

    def render_to_pdf(self, template_src, context_dict):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None


    def get(self, request):

        time_range = request.GET.get('time_range')

        # Define start and end dates based on the time range
        end_date = timezone.now()
        if time_range == '1_day':
            start_date = end_date - timedelta(days=1)
        elif time_range == '1_week':
            start_date = end_date - timedelta(weeks=1)
        elif time_range == '1_month':
            start_date = end_date - timedelta(days=30)

        # Fetch data from the model within the specified time range
        data = migrationData.objects.filter(created_at__range=(start_date, end_date))

        # Serialize the queryset to JSON
        json_data = serialize('json', data)

        # Convert JSON data to a Python dictionary
        data_dict = json.loads(json_data)

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Prepare data for the template
        context = {
            'data': data_dict,
            'time_range_label': f'{start_date_str} to {end_date_str}',
        }

        # Render the HTML template to a PDF
        pdf = self.render_to_pdf('pdf_template.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="data.pdf"'
            return response
        return HttpResponse("Error generating PDF", status=400)