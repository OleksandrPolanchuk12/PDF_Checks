from check.models import Check
from rest_framework import serializers

class CheckSerializers(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ('id', 'pdf', 'status')