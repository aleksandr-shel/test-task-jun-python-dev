from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from ..permissions import HasModelPerm

class CanViewOrders(HasModelPerm): perm = 'api.view_order'
class CanCreateOrders(HasModelPerm): perm = 'api.add_order'
class CanUpdateOrders(HasModelPerm): perm = 'api.change_order'
class CanDeleteOrders(HasModelPerm): perm = 'api.delete_order'

class OrdersListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [CanViewOrders()]
        if self.request.method == 'POST':
            return [CanCreateOrders()]
        return super().get_permissions()

    def get(self,request):
        return Response('list of orders')

    def post(self,request):

        return Response('add order')


class OrdersDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [CanViewOrders()]
        if self.request.method in ['PUT', 'PATCH']:
            return [CanUpdateOrders()]
        if self.request.method == 'DELETE':
            return [CanDeleteOrders()]
        return super().get_permissions()

    def get(self,request,pk):
        return Response(f'view order by id:{pk}')

    def delete(self,request,pk):
        return Response(f'delete order by id:{pk}')

    def patch(self,request,pk):
        return Response(f'update order by id:{pk}')
