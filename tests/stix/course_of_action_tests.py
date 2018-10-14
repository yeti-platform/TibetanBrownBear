"""Tests for the Stix2 bindings."""

import pytest

from stix2 import CourseOfAction as StixCourseOfAction

from yeti.core.entities.course_of_action import CourseOfAction


@pytest.mark.usefixtures('clean_db')
def test_course_of_action_creation():
    """Tests the creation of a single CourseOfAction object."""
    course_of_action = CourseOfAction(
        name='Add TCP port 80 Filter Rule to the existing Block UDP 1434 Filter',
        description='This is how you do it!'
    )
    # pylint: disable=protected-access
    assert course_of_action._stix_object is not None
    assert isinstance(course_of_action._stix_object, StixCourseOfAction)

@pytest.mark.usefixtures('clean_db')
def test_update_course_of_action():
    """Tests that a CourseOfAction object is succesfully updated."""
    course_of_action = CourseOfAction(
        name='Add TCP port 80 Filter Rule to the existing Block UDP 1434 Filter',
        description='This is how you do it!'
    )
    course_of_action.save()
    stix_id = course_of_action.id
    updated = course_of_action.update({'name': 'Add TCP port 8080 Filter Rule'})
    assert updated.name == 'Add TCP port 8080 Filter Rule'
    assert updated.id == stix_id
    assert updated.description == 'This is how you do it!'
