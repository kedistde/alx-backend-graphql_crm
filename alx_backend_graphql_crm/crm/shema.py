import graphene
import crm.schema

class Query(crm.schema.Query, graphene.ObjectType):
    # This will combine all queries from different apps
    pass

class Mutation(crm.schema.Mutation, graphene.ObjectType):
    # This will combine all mutations from different apps
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
