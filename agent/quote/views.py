import datetime
from dateutil.relativedelta import relativedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.db.models import Avg, Max, Min
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from .forms import PriceForm
from .models import Quote


def dashboard(request):
    """ Dashboard view to provide overview to agents
        Args:
            request <request object>: request object
        Returns:
            Dashboard template with new_quotes and completed_quotes template variables
    """
    new_quotes = Quote.objects.filter(new_quote=True)
    completed_quotes = Quote.objects.filter(new_quote=False)
    return render(
        request,
        'quote/dashboard.html',
        {'new_quotes': new_quotes, 'completed_quotes': completed_quotes}
    )


def new(request):
    """ New quotes view to provide current new quotes to agents
        Args:
            request <request object>: request object
        Returns:
            New quotes template with new_quotes template variable
    """
    new_quotes = Quote.objects.filter(new_quote=True)
    return render(request, 'quote/new.html', {'new_quotes': new_quotes})


def completed(request):
    """ Completed quotes view to provide completed quotes to agents
        Args:
            request <request object>: request object
        Returns:
            Completed quotes template with new_quotes and completed_quotes template variables
    """
    new_quotes = Quote.objects.filter(new_quote=True)
    completed_quotes = Quote.objects.filter(new_quote=False)
    return render(
        request,
        'quote/completed.html',
        {'completed_quotes': completed_quotes, 'new_quotes': new_quotes}
    )


class Price(View):
    """ Price CBV to allow agents to view quote details and enter quote values """
    def get(self, request, pk):
        """ View to allow agents to visualize quote details
            Args:
                request <request object>: request object
                pk <int>: primary key of quote to be visualized
            Returns:
                Quote detail template with price_form, quote, and new_quote template variables
        """
        new_quotes = Quote.objects.filter(new_quote=True)
        quote = Quote.objects.get(id=pk)
        price_form = PriceForm()

        current_datetime = datetime.datetime.now()
        current_timezone = timezone.get_current_timezone()
        non_naive_start_time = current_timezone.localize(current_datetime, is_dst=None)
        quote.start_time = non_naive_start_time
        quote.save()
        return render(
            request,
            'quote/price.html',
            {'price_form': price_form, 'quote': quote, 'new_quotes': new_quotes}
        )

    def post(self, request, pk):
        """ View to allow agents to enter quote value for a specific quote
            Args:
                request <request object>: request object
                pk <int>: primary key of quote to be adjusted with added price value
            Returns:
                New quotes template with new_quote template variable
        """
        new_quotes = Quote.objects.filter(new_quote=True)
        price_form = PriceForm(request.POST)
        if price_form.is_valid():
            price = price_form.cleaned_data['price_form']
        quote = Quote.objects.get(id=pk)
        quote.new_quote = False
        quote.price = price

        current_datetime = datetime.datetime.now()
        current_timezone = timezone.get_current_timezone()
        non_naive_end_time = current_timezone.localize(current_datetime, is_dst=None)
        quote.end_time = non_naive_end_time
        quote.save()
        return render(request, 'quote/new.html', {'new_quotes': new_quotes})


class AgentPerformance(APIView):
    """
    Agent Performance Information From Quote Data
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, pk, format=None):
        """ API endpoint to allow for collection of agent performance data
            Args:
                request <request object>: request object
                pk <int>: primary key of agent to be assessed
            Returns:
                JSON response of agent performance data
        """
        agent_quotes = Quote.objects.filter(new_quote=False).filter(customer__agent=pk)
        first_month = agent_quotes.earliest('end_time').end_time
        last_month = agent_quotes.latest('end_time').end_time

        date_list = []
        while first_month <= last_month:
            date_list.append(first_month)
            first_month += relativedelta(months=1)

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
                    'average': price_average,
                    'max': price_max,
                    'min': price_min,
                },
                'quote_time': {
                    'average': quote_completion_average,
                },
            }
        return Response(api_result)
