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
def test_execute():
    """Test that an existing feed can be executed"""
    rv = client.post('/api/async/FastDummyFeed/execute')
    response = json.loads(rv.data)
    assert response['status'] == 'queued'
    assert 'FastDummyFeed' in response['msg']
    # expecting a UUID: d18e0132-7271-4597-8fb3-8a2624f4059e
    assert re.match(r'[a-f0-9-]+', response['job_id'])

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_execute_duplicate():
    """Test that a feed cannot be run in parallel"""
    rv = client.post('/api/async/SlowDummyFeed/execute')
    rv = client.post('/api/async/SlowDummyFeed/execute')
    response = json.loads(rv.data)
    assert 'GenericYetiError' in response
    assert rv.status_code == 409
    assert '~"FastDummyFeed"' in response['GenericYetiError']

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_execute_nonexistent():
    """Test that executing a nonexistent feed generates an error."""
    rv = client.post('/api/async/nonexistent/execute')
    response = json.loads(rv.data)
    assert response['GenericYetiError'] == \
        'nonexistent is not a registered AsyncJob'
    assert rv.status_code == 404

@pytest.mark.usefixtures('clean_db')
def test_filter(populate_feeds):
    """Test that asyncJobs can be filtered by name."""
    rv = client.post('/api/async/filter', data={'name': 'DummyFeed'})
    response = json.loads(rv.data)
    assert len(response) == len(populate_feeds)

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_filter_errors():
    """Test that incorrect filtering generates a ValidationError / HTTP 400."""
    rv = client.post('/api/async/filter', data={})
    response = json.loads(rv.data)
    assert 'ValidationError' in response
    assert rv.status_code == 400

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_toggle():
    """Test that a feed can be toggled."""
    rv = client.post('/api/async/FastDummyFeed/toggle')
    response = json.loads(rv.data)
    assert response['enabled']
    assert 'FastDummyFeed' in response['msg']
    rv = client.post('/api/async/filter', data={'name': 'FastDummyFeed'})
    response = json.loads(rv.data)
    assert response[0]['enabled']
    rv = client.post('/api/async/filter', data={'name': 'SlowDummyFeed'})
    response = json.loads(rv.data)
    assert not response[0]['enabled']

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_toggle_nonexistent():
    """Test that toggling a nonexistent feed generates an error."""
    rv = client.post('/api/async/nonexistent/toggle')
    response = json.loads(rv.data)
    assert 'GenericYetiError' in response
    assert rv.status_code == 404

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_info():
    """Test that we can get information on a job."""
    rv = client.post('/api/async/FastDummyFeed/execute')
    response = json.loads(rv.data)
    assert 'job_id' in response
    jobid = response['job_id']
    time.sleep(0.1)
    rv = client.get('/api/async/info/' + jobid)
    response = json.loads(rv.data)
    assert response['meta']['name'] == 'FastDummyFeed'
    assert response['status'] in ['queued', 'started']

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_info_nonexistent():
    """Test that getting information on a nonexistent job generates an error."""
    rv = client.get('/api/async/info/d18e0132-0000-0000-0000-8a2624f4059e')
    response = json.loads(rv.data)
    assert 'GenericYetiError' in response
    assert response['GenericYetiError'] == \
        'Job ID d18e0132-0000-0000-0000-8a2624f4059e is not an active job'
    assert rv.status_code == 404

@pytest.mark.usefixtures('clean_db', 'populate_feeds')
def test_get_activejobs():
    """Test that getting information on a nonexistent job generates an error."""
    rv = client.post('/api/async/SlowDummyFeed/execute')
    time.sleep(0.1)
    rv = client.get('/api/async/active')
    response = json.loads(rv.data)
    assert len(response) == 1
