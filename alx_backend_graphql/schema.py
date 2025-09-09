import graphene
import crm.schema

class Query(crm.schema.Query, graphene.ObjectType):
    # This will inherit from the CRM app's Query class
    pass

schema = graphene.Schema(query=Query)

import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()
    
    def resolve_hello(self, info):
        return "Hello, GraphQL!"
