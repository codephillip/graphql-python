import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from links.models import Link, Vote
from users.schema import get_user


class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = ['url', 'description']


class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        interfaces = (graphene.relay.Node, )


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node, )


class RelayQuery(graphene.AbstractType):
    relay_link = graphene.relay.Node.Field(LinkNode)
    relay_links = DjangoFilterConnectionField(LinkNode, filterset_class=LinkFilter)


class RelayCreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNode)

    class Input:
        url = graphene.String()
        description = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):

        user = get_user(context) or None

        link = Link(
            url=input.get('url'),
            description=input.get('description'),
            posted_by=user,
        )
        link.save()

        return RelayCreateLink(link=link)


class RelayMutation(graphene.AbstractType):
    relay_create_link = RelayCreateLink.Field()
