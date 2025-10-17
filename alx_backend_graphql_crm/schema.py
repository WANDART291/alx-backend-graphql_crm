# alx_backend_graphql_crm/schema.py

import graphene
# Import Query and Mutation from the crm app
from crm.schema import Query as CRMQuery, Mutation as CRMMutation 

# Combine all Query classes
class Query(CRMQuery, graphene.ObjectType):
    pass 

# Combine all Mutation classes
class Mutation(CRMMutation, graphene.ObjectType):
    pass 

# Define the final schema object that urls.py imports
schema = graphene.Schema(query=Query, mutation=Mutation)