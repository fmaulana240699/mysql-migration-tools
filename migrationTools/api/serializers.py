from rest_framework import serializers
from .models import migrationData, repoIntegration, migrationConfig, Users

class migrationDataSerializer(serializers.ModelSerializer):
    sql_query = serializers.CharField(required=False)
    author = serializers.CharField(required=False)     

    class Meta:
        model = migrationData
        fields = '__all__' 

class migrationConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = migrationConfig
        fields = '__all__'      

    def create(self, validated_data):
        token = validated_data.pop('db_password')
        instance = self.Meta.model(**validated_data)
        instance.encrypt(token) 
        instance.save()
        return instance 

    def to_representation(self, instance):
        data = super().to_representation(instance)
        instance.decrypt()
        data['db_password'] = instance.db_password
        return data             
    
class repoIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = repoIntegration
        fields = '__all__'

    def create(self, validated_data):
        token = validated_data.pop('token')
        instance = self.Meta.model(**validated_data)
        instance.encrypt(token) 
        instance.save()
        return instance 

    def to_representation(self, instance):
        data = super().to_representation(instance)
        instance.decrypt()
        data['token'] = instance.token
        return data
 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password) 
        instance.save()
        return instance  