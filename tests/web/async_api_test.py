"""Tests for the AsyncJob web API."""

import json
import re
import time

import pytest

from yeti.webapp import app
from yeti.core.async import get_active_jobs

app.testing = True
client = app.test_client()

@pytest.yield_fixture(autouse=True)
def wait_for_jobs():
    """Faits for active jobs to complete before each test run."""
    while get_active_jobs():
        time.sleep(0.1)

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_execute(authenticated_client):
    """Test that an existing feed can be executed"""
    rv = authenticated_client.post('/api/async/FastDummyFeed/execute')
    response = json.loads(rv.data)
    assert response['status'] == 'queued'
    assert 'FastDummyFeed' in response['msg']
    # expecting a UUID: d18e0132-7271-4597-8fb3-8a2624f4059e
    assert re.match(r'[a-f0-9-]+', response['job_id'])

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_execute_duplicate(authenticated_client):
    """Test that a feed cannot be run in parallel"""
    rv = authenticated_client.post('/api/async/FastDummyFeed/execute')
    rv = authenticated_client.post('/api/async/FastDummyFeed/execute')
    rv = authenticated_client.post('/api/async/FastDummyFeed/execute')
    response = json.loads(rv.data)
    assert 'GenericYetiError' in response
    assert rv.status_code == 409
    assert '~"FastDummyFeed"' in response['GenericYetiError']

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_execute_nonexistent(authenticated_client):
    """Test that executing a nonexistent feed generates an error."""
    rv = authenticated_client.post('/api/async/nonexistent/execute')
    response = json.loads(rv.data)
    assert response['GenericYetiError'] == \
        'nonexistent is not a registered AsyncJob'
    assert rv.status_code == 404

@pytest.mark.usefixtures('clean_db')
def test_filter(populate_feeds, authenticated_client):
    """Test that asyncJobs can be filtered by name."""
    rv = authenticated_client.post('/api/async/filter', data={'name': 'DummyFeed'})
    response = json.loads(rv.data)
    assert len(response) == len(populate_feeds)

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_filter_errors(authenticated_client):
    """Test that incorrect filtering generates a ValidationError / HTTP 400."""
    rv = authenticated_client.post('/api/async/filter', data={})
    response = json.loads(rv.data)
    assert 'ValidationError' in response
    assert rv.status_code == 400

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_toggle(authenticated_client):
    """Test that a feed can be toggled."""
    rv = authenticated_client.post('/api/async/FastDummyFeed/toggle')
    response = json.loads(rv.data)
    assert response['enabled']
    assert 'FastDummyFeed' in response['msg']
    rv = authenticated_client.post('/api/async/filter', data={'name': 'FastDummyFeed'})
    response = json.loads(rv.data)
    assert response[0]['enabled']
    rv = authenticated_client.post('/api/async/filter', data={'name': 'SlowDummyFeed'})
    response = json.loads(rv.data)
    assert not response[0]['enabled']

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_toggle_nonexistent(authenticated_client):
    """Test that toggling a nonexistent feed generates an error."""
    rv = authenticated_client.post('/api/async/nonexistent/toggle')
    response = json.loads(rv.data)
    assert 'GenericYetiError' in response
    assert rv.status_code == 404

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_info(authenticated_client):
    """Test that we can get information on a job."""
    rv = authenticated_client.post('/api/async/FastDummyFeed/execute')
    response = json.loads(rv.data)
    assert 'job_id' in response
    jobid = response['job_id']
    time.sleep(0.1)
    rv = authenticated_client.get('/api/async/info/' + jobid)
    response = json.loads(rv.data)
    assert response['meta']['name'] == 'FastDummyFeed'
    assert response['status'] in ['queued', 'started']

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_info_nonexistent(authenticated_client):
    """Test that getting information on a nonexistent job generates an error."""
    rv = authenticated_client.get('/api/async/info/d18e0132-0000-0000-0000-8a2624f4059e')
    response = json.loads(rv.data)
    assert 'GenericYetiError' in response
    assert response['GenericYetiError'] == \
        'Job ID d18e0132-0000-0000-0000-8a2624f4059e is not an active job'
    assert rv.status_code == 404

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_get_activejobs(authenticated_client):
    """Test that getting information on a nonexistent job generates an error."""
    rv = authenticated_client.post('/api/async/SlowDummyFeed/execute')
    time.sleep(0.1)
    rv = authenticated_client.get('/api/async/active')
    response = json.loads(rv.data)
    assert len(response) == 1
