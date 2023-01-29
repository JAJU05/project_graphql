import graphene
from graphene_django import DjangoObjectType

from home.models import News


class NewsType(DjangoObjectType):
    class Meta:
        model = News


class NewsInput(graphene.InputObjectType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()


class Query(graphene.ObjectType):
    news = graphene.List(NewsType)
    new = graphene.Field(NewsType, id=graphene.Int())

    @graphene.resolve_only_args
    def resolve_news(self):
        return News.objects.all()

    @graphene.resolve_only_args
    def resolve_new(self, id):
        return News.objects.get(pk=id)


class CreateNews(graphene.Mutation):
    class Arguments:
        new_data = NewsInput(required=True)

    new = graphene.Field(NewsType)

    @staticmethod
    def mutate(root, info, new_data=None):
        new_instance = News(**new_data).save()
        return CreateNews(new=new_instance)


class UpdateNews(graphene.Mutation):
    class Arguments:
        new_data = NewsInput(required=True)

    new = graphene.Field(NewsType)

    @staticmethod
    def mutate(root, info, new_data=None):
        new_instance = News.objects.get(pk=new_data.id)
        if new_instance:

            new_instance.title = new_data.title
            new_instance.description = new_data.description
            new_instance.save()

            return UpdateNews(new=new_instance)  # noqa
        return UpdateNews(new=None)  # noqa


class DeleteNews(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    new = graphene.Field(NewsType)

    @staticmethod
    def mutate(root, info, id):
        News.objects.get(pk=id).delete()


class Mutation(graphene.ObjectType):
    create_new = CreateNews.Field()
    update_new = UpdateNews.Field()
    delete_new = DeleteNews.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)