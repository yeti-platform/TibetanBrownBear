"""Tests for the AsyncJob web API."""

import json
import re
import time

import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()

@pytest.mark.usefixtures("clean_db")
def test_execute(populate_feeds):
    """Test that an existing feed can be executed"""
    rv = client.post('/api/async/DummyFeed1/execute')
    response = json.loads(rv.data)
    assert response['status'] == 'queued'
    assert 'DummyFeed1' in response['msg']
    # expecting a UUID: d18e0132-7271-4597-8fb3-8a2624f4059e
    assert re.match(r'[a-f0-9-]+', response['job_id'])

@pytest.mark.usefixtures("clean_db")
def test_filter(populate_feeds):
    """Test that asyncJobs can be filtered by name."""
    rv = client.post('/api/async/filter', data={'name': 'DummyFeed'})
    response = json.loads(rv.data)
    print(response)
    assert len(response) == len(populate_feeds)

@pytest.mark.usefixtures("clean_db")
def test_filter_errors(populate_feeds):
    """Test that incorrect filtering generates a ValidationError / HTTP 400."""
    rv = client.post('/api/async/filter', data={})
    response = json.loads(rv.data)
    assert 'ValidationError' in response
    assert rv.status_code == 400

@pytest.mark.usefixtures("clean_db")
def test_toggle(populate_feeds):
    """Test that a feed can be toggled."""
    rv = client.post('/api/async/DummyFeed1/toggle')
    response = json.loads(rv.data)
    assert response['enabled']
    assert 'DummyFeed1' in response['msg']
    rv = client.post('/api/async/filter', data={'name': 'DummyFeed1'})
    response = json.loads(rv.data)
    assert response[0]['enabled']
    rv = client.post('/api/async/filter', data={'name': 'DummyFeed2'})
    response = json.loads(rv.data)
    assert not response[0]['enabled']
    
@pytest.mark.usefixtures("clean_db")
def test_info(populate_feeds):
    """Test that we can get information on a job."""
    rv = client.post('/api/async/DummyFeed1/execute')
    response = json.loads(rv.data)
    jobid = response['job_id']
    print (jobid)
    rv = client.get('/api/async/info/' + jobid)
    response = json.loads(rv.data)
    assert response['meta']['name'] == 'DummyFeed1'
    assert response['status'] == 'queued'
    time.sleep(2)
    rv = client.get('/api/async/info/' + jobid)
    response = json.loads(rv.data)
    assert response['meta']['name'] == 'DummyFeed1'
    assert response['status'] == 'finished'
