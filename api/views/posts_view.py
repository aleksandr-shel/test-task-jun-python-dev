from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from ..permissions import HasModelPerm

class CanViewPosts(HasModelPerm): perm = 'api.view_post'
class CanCreatePosts(HasModelPerm): perm = 'api.add_post'
class CanUpdatePosts(HasModelPerm): perm = 'api.change_post'
class CanDeletePosts(HasModelPerm): perm = 'api.delete_post'

class PostsListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()] #видно всем
        if self.request.method == 'POST':
            return [CanCreatePosts()] #
        return super().get_permissions()

    def get(self,request):
        return Response('list of posts')

    def post(self,request):

        return Response('add post')


class PostsDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [CanViewPosts()]
        if self.request.method in ['PUT', 'PATCH']:
            return [CanUpdatePosts()]
        if self.request.method == 'DELETE':
            return [CanDeletePosts()]
        return super().get_permissions()

    def get(self,request,pk):
        return Response(f'view post by id:{pk}')

    def delete(self,request,pk):
        return Response(f'delete post by id:{pk}')

    def patch(self,request,pk):
        return Response(f'update post by id:{pk}')
