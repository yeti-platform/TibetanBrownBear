"""Tests for the Stix2 bindings."""
import pytest

from stix2 import Report as StixReport
from yeti.core.entities.report import Report


@pytest.mark.usefixtures('clean_db')
def test_report_creation():
    """Tests the creation of a single Report object."""
    report = Report(
        name='The Black Vine Cyberespionage Group',
        description='A simple report with an indicator and campaign',
        labels=['campaign'],
        published='2016-01-20T17:00:00.000Z',
        object_refs=[
            'indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2',
            'campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c',
            'relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a'
        ],
    )
    # pylint: disable=protected-access
    assert report._stix_object is not None
    assert isinstance(report._stix_object, StixReport)

@pytest.mark.usefixtures('clean_db')
def test_update_report():
    """Tests that a Report object is succesfully updated."""

    report = Report(
        name='The Black Vine Cyberespionage Group',
        description='A simple report with an indicator and campaign',
        labels=['campaign'],
        published='2016-01-20T17:00:00.000Z',
        object_refs=[
            'indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2',
            'campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c',
            'relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a'
        ],
    )
    report.save()
    modified = report.modified
    stix_id = report.id
    updated = report.update({'name': 'The White Vine Cyberespionage Group'})
    assert updated.id == stix_id
    assert updated.name == 'The White Vine Cyberespionage Group'
    assert updated.description == 'A simple report with an indicator and campaign'
    assert updated.labels == ['campaign']
    assert str(updated.published) == '2016-01-20 17:00:00+00:00'
    assert updated.object_refs == [
        'indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2',
        'campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c',
        'relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a'
    ]
    assert modified < updated.modified
