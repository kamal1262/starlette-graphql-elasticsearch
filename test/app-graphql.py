from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from starlette.routing import Route
import graphene
from elasticsearch import Elasticsearch
import json 
from datetime import datetime

class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime(required= False)
    age = graphene.Int(required=False)


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    email = graphene.String(email=graphene.String(default_value="md.kamal.hossain@hotmail.com"))
    name = graphene.String(lastName=graphene.String(default_value="Hossain"))
    kamal = graphene.String(kamal=graphene.String(default_value="getting it from ES"))
    users =  graphene.List(User, first = graphene.Int())


    def resolve_users( self, info, first):
        return [
            User(username='Alice', last_login= datetime.today()), 
            User(username='Bob', last_login= datetime.today()), 
            User(username='Michael', last_login= datetime.today()), 

        ][:first]

    async def resolve_hello(self, info, name):
        # We can make asynchronous network calls here.
        return "Hello " + name

    def resolve_email(self, info, email):
        # We can make asynchronous network calls here.
        return "email: " + email

    def resolve_name(self, info, lastName):
        # We can make asynchronous network calls here.
        return "Surname: " + lastName

    def resolve_kamal(self, info, kamal):
        es = Elasticsearch(hosts=["localhost"])
        query_body = {
        "query": {
            "match": {
                "_id": 1
                }
            }
        }

        res = es.search(index="car", body=query_body)
        res = res['hits']['hits'][0]['_source']

        print(res)
        return res

class CreateUser(graphene.Mutation):

    class Arguments:
        username = graphene.String()
        age = graphene.Int()
    
    user = graphene.Field(User)

    def mutate(self, info, username, age):
        user_define = User(username = username, age = age)
        return CreateUser(user= user_define)

class Mutations(graphene.ObjectType):
    create_user =CreateUser.Field()

# schema=graphene.Schema(query=Query)

# result = schema.execute(
#     '''
#     {
#         hello (name: "hola")
#         email(email: "kamal@rea.com")
#         kamal
#     }
#     '''
# )
# result = schema.execute(
#     '''
#     {
#         users {
#             username
#             last_login
#         }
#     }
#     '''
# )


# item = dict(result.data.items())
# print(json.dumps(item, indent=4))

routes = [
    # We're using `executor_class=AsyncioExecutor` here.
    Route('/graphql', GraphQLApp(
        schema=graphene.Schema(query=Query, mutation=Mutations),
        executor_class=AsyncioExecutor
    ))
]

app = Starlette(routes=routes)

