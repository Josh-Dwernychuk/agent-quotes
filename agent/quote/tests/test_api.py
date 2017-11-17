import datetime
import json
import pytest

from django.utils import timezone

from agent.quote.tests.factories import AgentFactory, CustomerFactory, QuoteFactory


@pytest.mark.django_db
def test_api_get_request(admin_client):
    """ Test API request for agent and ensure proper data is returned """
    agent = AgentFactory(id=1)
    customer = CustomerFactory(agent=agent)

    current_timezone = timezone.get_current_timezone()
    start_time_1 = current_timezone.localize(
        datetime.datetime(2017, 9, 11, 7, 9, 22, 0), is_dst=None
    )
    start_time_2 = current_timezone.localize(
        datetime.datetime(2017, 11, 16, 4, 7, 10, 0), is_dst=None
    )
    start_time_3 = current_timezone.localize(
        datetime.datetime(2017, 11, 17, 4, 3, 12, 0), is_dst=None
    )
    end_time_1 = current_timezone.localize(
        datetime.datetime(2017, 9, 12, 7, 9, 22, 0), is_dst=None
    )
    end_time_2 = current_timezone.localize(
        datetime.datetime(2017, 11, 17, 4, 3, 11, 0), is_dst=None
    )
    end_time_3 = current_timezone.localize(
        datetime.datetime(2017, 11, 18, 4, 2, 14, 0), is_dst=None
    )
    QuoteFactory(
        customer=customer,
        new_quote=False,
        price=1.00,
        start_time=start_time_1,
        end_time=end_time_1
    )
    QuoteFactory(
        customer=customer,
        new_quote=False,
        price=2.00,
        start_time=start_time_2,
        end_time=end_time_2
    )
    QuoteFactory(
        customer=customer,
        new_quote=False,
        price=3.00,
        start_time=start_time_3,
        end_time=end_time_3
    )

    response = admin_client.get('http://localhost:8000/quote/performance/1/')
    assert response.status_code == 200
    assert json.loads(response.content.decode("utf-8"))["11/2017"]["quote_time"]["average"] == \
        86251.5
    assert json.loads(response.content.decode("utf-8"))["11/2017"]["price"]["average"] == 2.5
    assert json.loads(response.content.decode("utf-8"))["11/2017"]["price"]["max"] == 3.0
    assert json.loads(response.content.decode("utf-8"))["11/2017"]["price"]["min"] == 2.0
    assert json.loads(response.content.decode("utf-8"))["11/2017"]["quotes_finished"] == 2

    assert json.loads(response.content.decode("utf-8"))["10/2017"]["quote_time"]["average"] == 0
    assert json.loads(response.content.decode("utf-8"))["10/2017"]["price"]["average"] == 0
    assert json.loads(response.content.decode("utf-8"))["10/2017"]["price"]["max"] == 0
    assert json.loads(response.content.decode("utf-8"))["10/2017"]["price"]["min"] == 0
    assert json.loads(response.content.decode("utf-8"))["10/2017"]["quotes_finished"] == 0

    assert json.loads(response.content.decode("utf-8"))["9/2017"]["quote_time"]["average"] == \
        86400.0
    assert json.loads(response.content.decode("utf-8"))["9/2017"]["price"]["average"] == 1.0
    assert json.loads(response.content.decode("utf-8"))["9/2017"]["price"]["max"] == 1.0
    assert json.loads(response.content.decode("utf-8"))["9/2017"]["price"]["min"] == 1.0
    assert json.loads(response.content.decode("utf-8"))["9/2017"]["quotes_finished"] == 1
