from rest_framework import serializers

from .models import Cat, Owner


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cat
        fields = ('name', 'color', 'birth_year', 'owner')


class OwnerSerializer(serializers.ModelSerializer):
    # many - чтобы разрешить обработку списков, т.к. связь один-ко-многим
    # Тип StringRelatedField не поддерживает операции записи,
    # поэтому нужно всегда read_only=True
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
