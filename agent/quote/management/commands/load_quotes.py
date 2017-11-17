import codecs
import csv
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from agent.quote.models import Agent, Customer, Quote


class Command(BaseCommand):
    help = '''
        Loads sample quotes from CSV file

        args:
        overwrite (default: False) - if set to true, any rows which match
        existing objects in the database will be overwritten.

    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '-o', '--overwrite',
            dest='overwrite',
            action='store_true',
        )

    def handle(self, *args, **options):
        overwrite = options['overwrite']
        print('Overwrite: {}'.format(overwrite))

        with codecs.open(
            './agent/quote/data/quotes.csv',
            "r",
            encoding='utf-8',
            errors='ignore'
        ) as quotes_file:

            quotes = csv.reader(quotes_file)
            for row in quotes:
                if quotes.line_num == 1:  # header row
                    continue
                agent_name = row[0]
                customer_name = row[1]
                customer_type = row[2]
                address = row[3]
                new_quote = row[4]
                price = row[5]
                date = self.get_date(row[6])
                start_time = self.get_date(row[7])
                end_time = self.get_date(row[8])

                agent, created = Agent.objects.get_or_create(name=agent_name)

                customer, created = Customer.objects.get_or_create(
                    agent=agent,
                    name=customer_name,
                    customer_type=customer_type
                )

                quote, created = Quote.objects.get_or_create(
                    customer=customer,
                    address=address,
                    new_quote=new_quote,
                    price=price,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                )

                if created:
                    print('New Quote Created: {} - {}'.format(quote.customer.name, quote.address))

                if not created:
                    if overwrite:
                        # overwrite the values on the object
                        quote.cutomer = customer
                        quote.address = address
                        quote.new_quote = new_quote
                        quote.price = price
                        quote.date = date
                        quote.start_time = start_time
                        quote.end_time = end_time
                        quote.save()
                        print('Updated: {} - {}'.format(quote.customer.name, quote.address))
                    else:
                        print('Skipping update: {} - {}'.format(
                            quote.customer.name,
                            quote.address
                            )
                        )

    def get_date(self, str_date):
        """ Parse the datetime object into a formate that can be saved """
        if not str_date or str_date == 'None':
            return None
        else:
            date = datetime.datetime.strptime(str_date, '%Y-%m-%d:%H:%M:%S')
            current_timezone = timezone.get_current_timezone()
            non_naive_date_time = current_timezone.localize(date, is_dst=None)
            return non_naive_date_time
