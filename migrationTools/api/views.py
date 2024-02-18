from .models import migrationData, repoIntegration
from .serializers import migrationDataSerializer, repoIntegrationSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken, RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.forms.models import model_to_dict
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta, datetime
from django.http import JsonResponse
import json
from django.core.serializers import serialize
    
'''         
class PeminjamanListPerUserAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport ]

    queryset = Peminjaman.objects.all()
    serializer_class = PeminjamanSerializer

    def get(self, request, pk):
        try:
            list_peminjaman = Peminjaman.objects.filter(id_akun=pk)
            serialized_data = serialize("json", list_peminjaman)
            serialized_data = json.loads(serialized_data)
            return Response(serialized_data, status=200)
        except Barang.DoesNotExist:
            return Response({'message': 'Peminjaman tidak ditemukan'}, status=404)   

class PeminjamanListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport | IsKaryawan]

    queryset = Peminjaman.objects.all()
    serializer_class = PeminjamanSerializer

class PeminjamanListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport | IsKaryawan]

    queryset = Peminjaman.objects.all()
    serializer_class = CreatePeminjamanSerializer

    def post(self, request):
        data = request.data
        serializer = CreatePeminjamanSerializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            tanggal_pengembalian_str = validated_data["tanggal_pengembalian"].strftime('%Y-%m-%d')
            tanggal_peminjaman_str = validated_data["tanggal_peminjaman"].strftime('%Y-%m-%d')
            durasi = datetime.strptime(tanggal_pengembalian_str, '%Y-%m-%d').date() - datetime.strptime(tanggal_peminjaman_str, '%Y-%m-%d').date()
            validated_data["durasi_peminjaman"] = durasi.days
            validated_data["status_peminjaman"] = "Waiting Approval"

            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)   

'''

class repoCreateListAPIView(generics.ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    queryset = repoIntegration.objects.all()
    serializer_class = repoIntegrationSerializer 

class migrationCreateListAPIView(generics.ListCreateAPIView):
    queryset = migrationData.objects.all()
    serializer_class = migrationDataSerializer 