# crm/schema.py

import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from django.db import IntegrityError, transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from decimal import Decimal

# Ensure these imports match the models and filters you defined
from .models import Customer, Product, Order 
from .models import validate_phone_format 
from .filters import CustomerFilter, ProductFilter, OrderFilter 


# --- 1. Object Types (Output) ---

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter 
        interfaces = (graphene.relay.Node,) 

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)


# --- 2. Mutations (Input/Creation - Task 1 & 2) ---

class BaseMutation(graphene.relay.ClientIDMutation):
    message = graphene.String() 
    class Input:
        pass
        
    # FIX: This method is required by ClientIDMutation for all subclasses
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        raise NotImplementedError("Subclasses must implement mutate_and_get_payload") # Prevents base class from being called directly

# --- CreateCustomer Mutation ---
class CreateCustomer(BaseMutation):
    customer = graphene.Field(CustomerType)

    class Input:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        email = input.get('email')
        phone = input.get('phone')

        if Customer.objects.filter(email__iexact=email).exists():
            raise GraphQLError(f"Email '{email}' already exists. Please use a unique email.")

        if phone:
            try:
                validate_phone_format(phone)
            except DjangoValidationError as e:
                raise GraphQLError(f"Phone validation error: {e.message}")

        try:
            customer = Customer.objects.create(**input)
            return CreateCustomer(customer=customer, message="Customer created successfully.")
        except Exception as e:
            raise GraphQLError(f"An unexpected error occurred during creation: {str(e)}")


# --- BulkCreateCustomers Mutation (Challenge) ---
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)

class BulkCreateCustomers(BaseMutation):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String) 

    class Input:
        input = graphene.List(CustomerInput, required=True)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, input):
        valid_customers_data = []
        errors = []
        batch_emails = set()

        for i, data in enumerate(input):
            email = data.get('email')
            phone = data.get('phone')
            idx_msg = f"Record #{i+1} ({email or 'No Email'})"
            is_valid = True

            # Validation checks (Database, Batch, Phone Format)
            if Customer.objects.filter(email__iexact=email).exists():
                errors.append(f"{idx_msg}: Email '{email}' already exists.")
                is_valid = False
            
            if email in batch_emails:
                errors.append(f"{idx_msg}: Duplicate email within the current batch.")
                is_valid = False
            
            if phone:
                try:
                    validate_phone_format(phone)
                except DjangoValidationError as e:
                    errors.append(f"{idx_msg}: Phone validation error: {e.message}")
                    is_valid = False
            
            if is_valid:
                valid_customers_data.append(data)
                batch_emails.add(email)

        # Bulk create valid records
        if valid_customers_data:
            customers_to_create = [Customer(**data) for data in valid_customers_data]
            created_customers = Customer.objects.bulk_create(customers_to_create)
            return BulkCreateCustomers(customers=created_customers, errors=errors)
        else:
            return BulkCreateCustomers(customers=[], errors=errors)


# --- CreateProduct Mutation ---
class CreateProduct(BaseMutation):
    product = graphene.Field(ProductType)

    class Input:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int(required=False, default_value=0)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        price = input.get('price')
        stock = input.get('stock')

        if price <= Decimal('0'):
            raise GraphQLError("Price must be a positive number.")
        
        if stock < 0:
            raise GraphQLError("Stock cannot be a negative number.")

        try:
            product = Product.objects.create(**input)
            return CreateProduct(product=product, message="Product created successfully.")
        except Exception as e:
            raise GraphQLError(f"Error creating product: {str(e)}")


# --- CreateOrder Mutation (Challenge: Nested Creation and Calculation) ---
class CreateOrder(BaseMutation):
    order = graphene.Field(OrderType)

    class Input:
        customer_id = graphene.ID(required=True) 
        product_ids = graphene.List(graphene.ID, required=True) 
        order_date = graphene.DateTime(required=False)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        customer_id = input.get('customer_id')
        product_ids = input.get('product_ids')

        if not product_ids:
            raise GraphQLError("Order must include at least one product.")
        
        # 1. Check Customer Existence
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise GraphQLError(f"Customer with ID '{customer_id}' does not exist.")

        # 2. Check Products Existence
        products_queryset = Product.objects.filter(pk__in=product_ids)
        if products_queryset.count() != len(product_ids):
            existing_pks = set(str(p.pk) for p in products_queryset)
            missing_ids = [p_id for p_id in product_ids if str(p_id) not in existing_pks]
            raise GraphQLError(f"One or more products not found. Missing IDs: {', '.join(missing_ids)}.")

        # 3. Create Order Object
        order = Order.objects.create(
            customer=customer,
            order_date=input.get('order_date')
        )

        # 4. Associate Products
        order.products.set(products_queryset)

        # 5. Calculate and Update Total Amount
        total_amount = order.calculate_total()
        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])

        return CreateOrder(order=order, message="Order created successfully.")


# --- 3. Query and Mutation Definitions ---

class Query(graphene.ObjectType):
    # This maintains the hello query from Task 0
    hello = graphene.String(default_value="Hello, CRM GraphQL!") 

    # Task 3: Use DjangoFilterConnectionField for filtering, pagination, and sorting
    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)
    
    # Single object lookups
    customer = graphene.Field(CustomerType, id=graphene.ID())
    product = graphene.Field(ProductType, id=graphene.ID())

    def resolve_customer(root, info, id):
        try:
            return Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return None

    def resolve_product(root, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

class Mutation(graphene.ObjectType):
    # Register all mutations here
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()