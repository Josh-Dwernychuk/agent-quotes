from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.shortcuts import render
from django.views import View

from .forms import PriceForm
from .models import Quote
from .utils import create_non_naive_date_time, create_date_list, build_api_result


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
        quote.start_time = create_non_naive_date_time()
        quote.save()

        price_form = PriceForm()

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
        quote.end_time = create_non_naive_date_time()
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
        date_list = create_date_list(agent_quotes)
        api_result = build_api_result(date_list, pk)
        return Response(api_result)
