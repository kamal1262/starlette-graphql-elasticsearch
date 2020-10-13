import graphene


class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    last_login = graphene.DateTime()
