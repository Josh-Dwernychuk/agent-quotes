from django.urls import reverse


def test_dashboard(admin_client):
    """ Test dashboard view and ensure a proper repsonse """
    response = admin_client.get(reverse('quote:dashboard'))
    assert response.status_code == 200
    assert 'Quote Management Dashboard' in str(response.content)
    assert 'New Quotes' in str(response.content)
    assert 'Completed Quotes' in str(response.content)
    assert 'Full Name' in str(response.content)
    assert 'Address' in str(response.content)
    assert 'Customer Type' in str(response.content)
    assert 'Quote Price' in str(response.content)


def test_new_quotes(admin_client):
    """ Test new quotes view and ensure a proper repsonse """
    response = admin_client.get(reverse('quote:new'))
    assert response.status_code == 200
    assert 'Dashboard' in str(response.content)
    assert 'Completed Quotes' in str(response.content)
    assert 'New Quotes' in str(response.content)


def test_completed_quotes(admin_client):
    """ Test completed quotes view and ensure a proper repsonse """
    response = admin_client.get(reverse('quote:completed'))
    assert response.status_code == 200
    assert 'Dashboard' in str(response.content)
    assert 'Completed Quotes' in str(response.content)
    assert 'New Quotes' in str(response.content)
