import graphene
import datetime

from starlette.routing import Route
from starlette.graphql import GraphQLApp

from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from werkzeug.utils import import_string
from starlette.applications import Starlette
from graphql.execution.executors.asyncio import AsyncioExecutor


class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    last_login = graphene.DateTime()


class Query(graphene.ObjectType):
    users = graphene.List(User)
    msg = graphene.String(name=graphene.String(default_value="stranger"))
    is_exist = graphene.Boolean(boolean=graphene.Boolean(default_value=True))

    async def resolve_users(self, info):
        return [
            User(name="Nazmi", last_login=datetime.datetime.now()),
            User(
                name="Ali",
                last_login=datetime.datetime.now() - datetime.timedelta(days=3),
            ),
            User(
                name="Bob",
                last_login=datetime.datetime.now() - datetime.timedelta(days=120),
            ),
        ]

    async def resolve_msg(self, info, name):
        return "Hello " + name

    async def resolve_is_exist(self, info, boolean):
        return boolean


class CreateUser(graphene.Mutation):
    class Arguments(object):
        name = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, name):
        user = User(name=name)
        return CreateUser(user)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()


middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=["*.rea-asia.com"]),
    Middleware(HTTPSRedirectMiddleware),
]

# from .modules.query import Queries

schema = graphene.Schema(query=Query, mutation=Mutations)
routes = [Route("/", GraphQLApp(schema=schema, executor_class=AsyncioExecutor),)]


def create_app(object_name):
    app = Starlette(routes=routes)
    app.config = import_string(object_name)

    return app
