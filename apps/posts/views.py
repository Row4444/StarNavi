import copy
from datetime import timedelta, datetime
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Like
from .permisions import IsOwner

from .serializers import (
    PostSerializer,
    LikeSerializer,
    AnalyticsSerializer,
)


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class LikeCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, **self.kwargs)
        if not Like.objects.filter(author=self.request.user, post=post).exists():
            serializer.save(author=self.request.user, post=post)


class LikeDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsOwner]

    def get_object(self):
        post = get_object_or_404(Post, **self.kwargs)
        like = get_object_or_404(post.like_set, author=self.request.user)
        self.check_object_permissions(self.request, like)
        return like


class PostsAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_dates(self) -> list:
        date_from = self.request.GET.get("date_from", False)
        date_to = self.request.GET.get("date_to", False)
        if date_from and date_to:
            try:
                date_from_date = datetime.strptime(date_from, "%Y-%m-%d")
                date_to_date = datetime.strptime(date_to, "%Y-%m-%d")
                if date_to_date > date_from_date:
                    range_days = (date_to_date - date_from_date).days
                    return [(date_from_date + timedelta(days=i)) for i in range(range_days + 1)]
            except ValueError:
                pass
        return []

    def make_response(self) -> list:
        dates = self.get_dates()
        response = [
            {
                day.strftime("%Y-%m-%d"): AnalyticsSerializer(
                    Post.objects.filter(author=self.request.user),
                    context={"date": day},
                    many=True,
                ).data
            }
            for day in dates
        ]
        return response

    def get(self, request, *args, **kwargs):
        response = self.make_response()
        if not response:
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        return Response(response, status=status.HTTP_200_OK)
