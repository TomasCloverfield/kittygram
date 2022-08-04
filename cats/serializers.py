import datetime as dt

from rest_framework import serializers
# import webcolors

from .models import Cat, Owner, Achievement, AchievementCat, CHOICES


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


# class Hex2NameColor(serializers.Field):
#     def to_representation(self, value):
#         # При чтении данных ничего не меняем - просто возвращаем как есть
#         return value
#
#     def to_internal_value(self, data):
#         try:
#             data = webcolors.hex_to_name(data)
#         except ValueError:
#             raise serializers.ValidationError('No name for this HEX color')
#         return data


class CatSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(many=True, required=False)
    age = serializers.SerializerMethodField()
    # color = Hex2NameColor()
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = (
            'name', 'color', 'birth_year', 'owner', 'achievements', 'age'
        )

    def create(self, validated_data):
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat

        # Уберем список достижений из словаря validated_data и сохраним его
        achievements = validated_data.pop('achievements')

        # Создадим нового котика пока без достижений, данных нам достаточно
        cat = Cat.objects.create(**validated_data)

        for achievement in achievements:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement
            )
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat
            )
        return cat

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year


class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')


class OwnerSerializer(serializers.ModelSerializer):
    # # many - чтобы разрешить обработку списков, т.к. связь один-ко-многим
    # # Тип StringRelatedField не поддерживает операции записи,
    # # поэтому нужно всегда read_only=True
    # cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')


# Примеры из задания
# 1
# class PostSerializer(serializers.ModelSerializer):
#     group = serializers.SlugRelatedField(
#         queryset=Group.objects.all(),
#         slug_field='slug',
#         required=False
#     )
#
#     class Meta:
#         fields = ('id', 'text', 'author', 'image', 'pub_date', 'group')
#         model = Post
# 2
# from rest_framework import serializers
#
# from .models import Group, Post, Tag, TagPost
#
# # опишите сериализатор для хештегов
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('name', )
#
#
# class PostSerializer(serializers.ModelSerializer):
#     group = serializers.SlugRelatedField(slug_field='slug',
#             queryset=Group.objects.all(), required=False)
#     tag = TagSerializer(many=True, required=False)
#
#     class Meta:
#         fields = ('id', 'text', 'author', 'image', 'pub_date', 'group', 'tag')
#         model = Post
#
#     def create(self, validated_data):
#         if 'tag' not in self.initial_data:
#             post = Post.objects.create(**validated_data)
#             return post
#         tags = validated_data.pop('tag')
#         post = Post.objects.create(**validated_data)
#         for tag in tags:
#             current_tag, status = Tag.objects.get_or_create(**tag)
#             TagPost.objects.create(tag=current_tag, post=post)
#         print(post)
#         return post