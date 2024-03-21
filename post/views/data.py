from rest_framework.views import APIView
from rest_framework.response import Response
from post.models import Post
from post.serializers import PostModelSerializer
from rest_framework import status
from rest_framework import permissions

import traceback

class PostingView(APIView):
    permission_classes= [permissions.IsAuthenticated]
    def post(self, request, *agrs, **kwargs):
        try:
            data = request.data
            data['user'] = request.user.user_id
            data['created_on']='2024-03-13'
            ser = PostModelSerializer(data=data)
            if ser.is_valid():
                ser.save()
                return Response(
                    {"status": "success", "data": {"Post": ser.data}},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(ser.errors, status=413)
        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=500)

    def get(self, request, *agrs, **kwargs):
        try:
            posts = Post.objects.filter(user=request.user)
            ser = PostModelSerializer(posts, many=True)
            post_titles = []
            for post_data in ser.data:
                post_title = post_data.get('post_title')  # Use .get() to avoid KeyError
            if post_title is not None:
                post_titles.append(post_title)
            return Response(
                    {"status": "success", "post_titles": post_titles
                    }, status=200
            )
        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=500)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
            serializer = PostModelSerializer(instance=post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": "success", "data": {"Post": serializer.data}},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
            post.delete()
            return Response(
                {"status": "success", "message": "Post deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
