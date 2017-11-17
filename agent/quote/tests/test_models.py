import datetime
import pytest

from django.utils import timezone

from agent.quote.tests.factories import AgentFactory, CustomerFactory, QuoteFactory


@pytest.mark.django_db
def test_agent_creation():
    """ Test creation of agent model and ensure proper database entry is created """
    agent = AgentFactory()
    agent.name = 'agent test name'
    agent.save()
    assert agent.name == 'agent test name'


@pytest.mark.django_db
def test_customer_creation():
    """ Test creation of customer model and ensure proper database entries are created """
    agent = AgentFactory()
    customer = CustomerFactory(agent=agent)
    assert agent == customer.agent

    customer.name = 'customer test name 1'
    customer.customer_type = 'hom'
    customer.save()
    assert customer.name == 'customer test name 1'

    customer.name = 'customer test name 2'
    customer.customer_type = 'oth'
    customer.save()
    assert customer.name == 'customer test name 2'


@pytest.mark.django_db
def test_quote_creation():
    """ Test creation of quote model and ensure proper database entries are created """
    agent = AgentFactory()
    customer = CustomerFactory(agent=agent)
    quote = QuoteFactory(customer=customer)
    assert quote.customer.agent == agent
    assert quote.customer == customer

    quote.address = "123 Test St. Newark, CA"
    quote.new_quote = True
    quote.price = 100.00

    current_timezone = timezone.get_current_timezone()
    quote.date = current_timezone.localize(
        datetime.datetime(2017, 11, 17, 7, 6, 12, 0), is_dst=None
    )
    quote.start_time = current_timezone.localize(
        datetime.datetime(2017, 11, 17, 7, 8, 43, 0), is_dst=None
    )
    quote.end_time = current_timezone.localize(
        datetime.datetime(2017, 11, 17, 7, 9, 22, 0), is_dst=None
    )
    quote.save()

    assert quote.address == "123 Test St. Newark, CA"
    assert quote.new_quote is True
    assert quote.price == 100.00
    assert quote.date == current_timezone.localize(
        datetime.datetime(2017, 11, 17, 7, 6, 12, 0), is_dst=None
    )
    assert quote.start_time == current_timezone.localize(
        datetime.datetime(2017, 11, 17, 7, 8, 43, 0), is_dst=None
    )
    assert quote.end_time == current_timezone.localize(
        datetime.datetime(2017, 11, 17, 7, 9, 22, 0), is_dst=None
    )
