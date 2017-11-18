import datetime
from dateutil.relativedelta import relativedelta

from django.db.models import Avg, Max, Min
from django.utils import timezone

from .models import Quote


def create_non_naive_date_time():
    """ Method to create non naive date time
        Args:
            None
        Returns:
            non_naive_date_time <datetime object>: non naive date time object
    """
    current_datetime = datetime.datetime.now()
    current_timezone = timezone.get_current_timezone()
    non_naive_date_time = current_timezone.localize(current_datetime, is_dst=None)
    return non_naive_date_time


def create_date_list(agent_quotes):
    """ Method to create date list
        Args:
            agent_quotes <QuerySet object>: QuerySet of Quote model instances
        Returns:
            date_list <li>: List of monthly dates
                within date range of all quotes for specific agent
    """
    first_month = agent_quotes.earliest('end_time').end_time
    last_month = agent_quotes.latest('end_time').end_time

    date_list = []
    while first_month <= last_month:
        date_list.append(first_month)
        first_month += relativedelta(months=1)
    return date_list


def build_api_result(date_list, pk):
    """ Method to build API result for agent performance
        Args:
            date_list <li>: List of monthly dates
                within date range of all quotes for specific agent
            pk <int>: primary key to represent queried agent
        Returns:
            api_result <JSON>: Agent performance JSON data by month
    """
    api_result = {}
    for date in date_list:
        agent_quotes = Quote.objects.filter(
            new_quote=False
            ).filter(
            customer__agent=pk
            ).filter(
            end_time__month=date.month
            ).filter(
            end_time__year=date.year
        )
        quotes_finished = agent_quotes.count()
        if quotes_finished:
            price_average = agent_quotes.aggregate(Avg('price'))['price__avg']
            price_max = agent_quotes.aggregate(Max('price'))['price__max']
            price_min = agent_quotes.aggregate(Min('price'))['price__min']

            quote_completion_total = 0
            for agent_quote in agent_quotes:
                quote_completion_total += \
                    (agent_quote.end_time - agent_quote.start_time).total_seconds()
            quote_completion_average = quote_completion_total/float(quotes_finished)
        else:
            price_average = 0
            price_max = 0
            price_min = 0
            quote_completion_average = 0

        api_result[str(date.month) + '/' + str(date.year)] = {
            'quotes_finished': quotes_finished,
            'price': {
                'average': round(price_average),
                'max': round(price_max),
                'min': round(price_min),
            },
            'quote_time': {
                'average': round(quote_completion_average),
            },
        }
    return api_result
