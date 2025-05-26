from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from companies.models import Category, Company, Job, Tag, User, Comment


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ItemSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = instance.image.url if instance.image else ''
        return data

class CompanySerializer(ItemSerializer):
     class Meta:
        model = Company
        fields = ['id', 'name', 'created_date', 'category_id', 'image']

class JobSerializer(ItemSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'created_date', 'company_id', 'image']
#

#

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class JobDetailSerializer(JobSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = JobSerializer.Meta.model
        fields = JobSerializer.Meta.fields + ['title', 'tags']

class UserSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar.url if instance.avatar else ''
        return data
    # 'role'
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True

            }}

    #
    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u

class CommentSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        return data

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_date', 'updated_date', 'job']
        extra_kwargs = {
            'job': {
                'write_only': True
            }
        }



#
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['id', 'title', 'content', 'created_date', 'author']
#
#         read_only_fields = ['author', 'created_date']


