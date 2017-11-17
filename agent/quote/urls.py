from django.conf.urls import url
import agent.quote.views as views

urlpatterns = [
    url(r'^performance/(?P<pk>[0-9]+)/$', views.AgentPerformance.as_view()),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^new/$', views.new, name='new'),
    url(r'^completed/$', views.completed, name='completed'),
    url(r'^price/(?P<pk>[0-9]+)/$', views.Price.as_view(), name='price'),
    url(r'^price/$', views.Price, name='price_no_vars'),
]
