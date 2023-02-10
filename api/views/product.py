from django.forms import ValidationError
from rest_framework.response import Response
from api.serializers.product import (
    CustomerProductDetailSerializer,
    CustomerProductSerializer,
    ProductSerializer,
)
from rest_framework.views import exception_handler

from rest_framework.generics import ListAPIView, RetrieveAPIView

from product.models import CustomerProduct, Product,ProductMultiprice
from rest_framework.viewsets import ModelViewSet

class ProductMultipriceapi(ListAPIView):
    def get(self, request):
        try:
            products_list = Product.objects.all().values(
        "id",
        "title",
        "slug",
        "description",
        "image",
        "price",
        "is_taxable",
        "product_id",
        "unit",
        "category",
        "barcode"
        )
            temp_data = products_list
            for index,item in enumerate(products_list):
                print(item["id"])
                queryset = ProductMultiprice.objects.filter(product_id=item["id"]).values()
                temp_data[index]["multiprice"]=queryset
            return Response(temp_data,200)

        except Exception as error:
            return Response({"message":str(error)})






class ProductList(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = None

    def get_queryset(self):
        return Product.objects.active()


class ProductDetail(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Product.objects.active()


class CustomerProductAPI(ModelViewSet):
    serializer_class = CustomerProductSerializer
    queryset = CustomerProduct.objects.active()

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        is_added = CustomerProduct.objects.filter(
            is_deleted=False,
            status=True,
            customer=request.data["customer"],
            product=request.data["product"],
        )

        if not is_added:
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"message": "This product is already added to the customer"},
            )

    def get_queryset(self, *args, **kwargs):
        customer_id = self.request.query_params.get("customerId")
        if customer_id:
            queryset = CustomerProduct.objects.filter(
                is_deleted=False, status=True, customer=customer_id
            )

            return queryset
        else:
            return super().get_queryset()

    def get_serializer_class(self):
        detail_actions = ["retrieve", "list"]
        if self.action in detail_actions:
            return CustomerProductDetailSerializer
        return super().get_serializer_class()
