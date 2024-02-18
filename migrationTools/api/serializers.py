from rest_framework import serializers
from .models import migrationData, repoIntegration

class migrationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = migrationData
        fields = '__all__'
    
class repoIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = repoIntegration
        fields = '__all__'