from unicodedata import category
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


from product.models import CustomerProduct, Product, ProductCategory,ProductMultiprice


class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "title", "slug", "description"]

class ProductMultipriceSerializer(ModelSerializer):
    class Meta:
        model = ProductMultiprice




class ProductSerializer(ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = [
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
            "barcode",
        ]


class CustomerProductSerializer(ModelSerializer):
    class Meta:
        model = CustomerProduct
        fields = [
            "product",
            "customer",
            "price",
        ]


class PriceLessProductSerializer(ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "image",
            "is_taxable",
            "product_id",
            "unit",
            "category",
        ]


class CustomerProductDetailSerializer(ModelSerializer):
    product = PriceLessProductSerializer()
    agent = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = CustomerProduct
        fields = [
            "product",
            "price",
            "customer",
            "agent",
        ]

        optional_fields = ["agent"]

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        product_representation = representation.pop("product")
        for key in product_representation:
            representation[key] = product_representation[key]

        return representation

    def to_internal_value(self, data):
        product_internal = {}
        for key in PriceLessProductSerializer.Meta.fields:
            if key in data:
                product_internal[key] = data.pop(key)
        internal = super().to_internal_value(data)
        internal["product"] = product_internal
        return internal
