from gc import get_objects

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

# from unicodedata import category

from companies import serializers, paginators, perms
from rest_framework import viewsets, generics, status, parsers, permissions
from companies.models import Category, Company, Job, Tag, User, Comment

from  django.shortcuts import get_object_or_404
# from companies.perms import IsUserAndOwner


# from companies.serializers import PostSerializer
# from companies.perms import IsAdminOrEmployerOwnerOrReadOnly


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializer

class CompanyViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Company.objects.filter(active=True)
    serializer_class = serializers.CompanySerializer
    pagination_class = paginators.ItemPaginator

    def get_queryset(self):
        query = self.queryset
        q = self.request.query_params.get('q')
        if q:
            query = query.filter(name__icontains=q)

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            query = query.filter(category_id=cate_id)

        return query

    @action(methods = ['get'], detail = True, url_path = 'jobs')
    def get_jobs(self, request, pk):
        jobs= self.get_object().job_set.filter(active=True)
        return Response(serializers.JobSerializer(jobs, many=True).data, status=status.HTTP_200_OK)

class JobViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Job.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.JobDetailSerializer

    def get_permissions(self):
        if self.action in ['get_comments'] and self.request.method.__eq__('POST'):
            return [permissions.IsAuthenticated()]

        #
        # if self.action in ['create', 'update', 'destroy']:
        #     return [permissions.IsAuthenticated(),IsUserAndOwner()]
        #

        return [permissions.AllowAny()]

    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #

    @action(methods = ['get', 'post'], detail = True, url_path = 'comments')
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            s = serializers.CommentSerializer(data = {
                'user': request.user.pk,
                'job': pk,
                'content': request.data.get('content')
            })

            s.is_valid(raise_exception = True)
            c = s.save()
            return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

        comments = self.get_object().comment_set.select_related('user').filter(active=True)
        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

#
    # permission_classes = [IsAuthenticated, IsAdminOrEmployerOwnerOrReadOnly]
    #
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
#


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]


    @action(methods = ['get', 'patch'], url_path='current-user', detail = False,permission_classes = [permissions.IsAuthenticated])
    def get_current_user(self, request):
        u = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                if k in ['first_name', 'last_name']:
                    setattr(u, k, v)
                elif k.__eq__('password'):
                    u.set_password(v)
            # u.first_name = request.data.get['first_name']
            # u.last_name = request.data['last_name']
            u.save()
        return Response(serializers.UserSerializer(u).data)

class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.CommentOwner]


class ApproveUserView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        profile = get_object_or_404(Company, pk=pk)
        profile.is_approved = True
        profile.save()
        return Response({"message": "approved successfully"})
#




