import graphene
from graphene_django import DjangoObjectType
from django.db import models
from crm.models import Product, Customer, Order  # Add Product import

# Define ObjectTypes
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

# Queries
class Query(graphene.ObjectType):
    hello = graphene.String()
    products = graphene.List(ProductType)
    customers = graphene.List(CustomerType)
    orders = graphene.List(OrderType)
    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Float()
    
    def resolve_hello(self, info):
        return "Hello from GraphQL!"
    
    def resolve_products(self, info):
        return Product.objects.all()
    
    def resolve_customers(self, info):
        return Customer.objects.all()
    
    def resolve_orders(self, info):
        return Order.objects.all()
    
    def resolve_total_customers(self, info):
        return Customer.objects.count()
    
    def resolve_total_orders(self, info):
        return Order.objects.count()
    
    def resolve_total_revenue(self, info):
        return Order.objects.aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0

# Mutations
class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass
    
    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(graphene.String)
    
    def mutate(self, info):
        # Get products with stock less than 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []
        
        for product in low_stock_products:
            old_stock = product.stock
            product.stock += 10  # Increment stock by 10
            product.save()
            updated_products.append(f"{product.name}: {old_stock} -> {product.stock}")
        
        return UpdateLowStockProducts(
            success=True,
            message=f"Updated {len(updated_products)} products with low stock",
            updated_products=updated_products
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
