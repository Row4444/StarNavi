from abc import ABC

from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from apps.posts.models import Post, Like
from apps.users.serializers import UserSerializer

read_only_fields = ('author',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'date_of_like',)
        read_only_fields = ('post',)


class PostSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name="post_detail", read_only=True)
    user_can_like = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            "url",
            "id",
            "author",
            "title",
            "body",
            "date_of_create",
            "likes_count",
            "user_can_like",
        )
        read_only_fields = ('author', 'id')

    def get_likes_count(self, obj):
        return Like.objects.select_related("post").filter(post=obj).count()

    def get_user_can_like(self, obj):
        request = self.context.get("request")
        if request.user.is_authenticated:
            return not Like.objects.select_related("user", "post").filter(
                author=request.user,
                post=obj,
            ).exists()
        return False


class AnalyticsSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(source='id')
    title = serializers.CharField(max_length=64)
    like_count = serializers.SerializerMethodField(read_only=True)

    def get_like_count(self, obj):
        return Like.objects.select_related("post").filter(post=obj, date_of_like__date=self.context["date"]).count()



# [
#    {
#         2012-08-04: [
#             {
#                 post_id : 1,
#                 title : title1,
#                 likes_count : 123
#             },
#             {
#                 post_id : 2,
#                 title : title2,
#                 likes_count : 23
#                 }
#             }
#         ]
#    },
#    {
#         2012-08-05: [
#             {
#                 post_id : 1,
#                 title : title1,
#                 likes_count : 123
#             },
#             {
#                 post_id : 2,
#                 title : title2,
#                 likes_count : 23
#                 }
#            }
#         [
#     }
# ]

