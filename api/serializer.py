from rest_framework import serializers
from .models import blog,comment

class blogSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog
        fields = '__all__'


class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = '__all__'


