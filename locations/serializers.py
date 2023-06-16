from rest_framework import serializers
from .models import Location
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    email= serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
         )
    username=serializers.CharField(
        required=True,
        max_length=32,
        validators= [UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        required=True,
        max_length=32,
    )
    last_name= serializers.CharField(
        required=True,
        max_length=32,
    )
    password=serializers.CharField(
        required=True,
        min_length=8,
        write_only=True
    )
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
       model=User
       fields = (
       'token', 
       'username', 
       'password', 
       'first_name', 
       'last_name', 
       'email', 
       'id'
       )



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
