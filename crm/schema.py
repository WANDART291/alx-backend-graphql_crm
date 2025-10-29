# crm/schema.py

import graphene
from graphene_django import DjangoObjectType
from django.db import transaction

# Assuming your product model is imported/available here
from crm.models import Product # <-- ENSURE THIS IMPORT IS CORRECT

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'stock') # Include fields you want to return

class UpdateLowStockProducts(graphene.Mutation):
    """Mutation to restock products with stock < 10."""
    class Arguments:
        # We don't need input arguments as the criteria (stock < 10) is fixed
        pass

    # Fields the mutation returns
    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    @staticmethod
    def mutate(root, info):
        # Use a transaction to ensure atomic updates
        with transaction.atomic():
            
            # 1. Find all products with stock less than 10
            low_stock_products = Product.objects.filter(stock__lt=10)
            
            updated_list = []
            
            # 2. Increment stock by 10 for each product
            for product in low_stock_products:
                old_stock = product.stock
                product.stock += 10 # Restock by 10
                product.save()
                updated_list.append(product)
            
            if updated_list:
                msg = f"Successfully restocked {len(updated_list)} product(s)."
            else:
                msg = "No products required restocking."
                
        return UpdateLowStockProducts(
            success=True,
            message=msg,
            updated_products=updated_list
        )

# Ensure your main Mutation class includes the new field
class Mutation(graphene.ObjectType):
    # ... other mutations (e.g., createCustomer, updateOrder)
    update_low_stock_products = UpdateLowStockProducts.Field()
    # ...
