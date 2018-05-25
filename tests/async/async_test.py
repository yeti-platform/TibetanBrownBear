"""Tests for the Entity object."""
from datetime import timedelta

import pytest


@pytest.mark.usefixtures('clean_db')
def test_async_feed_info_fetch(populate_feeds):
    """Tests that a feed's meta information is correctly stored."""
    db_dummy_1 = populate_feeds[0]
    db_dummy_2 = db_dummy_1.__class__()
    assert db_dummy_1.settings.last_executed == db_dummy_2.settings.last_executed

@pytest.mark.usefixtures('clean_db')
def test_async_feed_info_update(populate_feeds):
    """Tests that updates to the feed's settings information are saved."""
    db_dummy_1 = populate_feeds[0]
    db_dummy_1.settings.period = timedelta(seconds=123)
    db_dummy_1.settings.enabled = True
    db_dummy_1.save_settings()
    new_db_dummy = db_dummy_1.__class__()
    assert new_db_dummy.settings.last_executed == db_dummy_1.settings.last_executed
    assert new_db_dummy.settings.period == timedelta(seconds=123)
    assert new_db_dummy.settings.enabled
