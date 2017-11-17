import factory

from agent.quote.models import Agent, Customer, Quote


class AgentFactory(factory.DjangoModelFactory):
    """
        Define Agent Factory
    """
    class Meta:
        model = Agent


class CustomerFactory(factory.DjangoModelFactory):
    """
        Define Customer Factory
    """
    class Meta:
        model = Customer

    agent = factory.SubFactory(AgentFactory)


class QuoteFactory(factory.DjangoModelFactory):
    """
        Define Quote Factory
    """
    class Meta:
        model = Quote

    customer = factory.SubFactory(CustomerFactory)
