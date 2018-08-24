"""Tests for the Stix2 bindings."""

import pytest

from stix2 import Tool as StixTool

from yeti.core.entities.tool import Tool


@pytest.mark.usefixtures('clean_db')
def test_tool_creation():
    """Tests the creation of a single Tool object."""
    tool = Tool(
        name='asd', labels=['label1'], tool_version='1.0', kill_chain_phases=[
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'testing'},
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'debugging'}
        ]
    )
    # pylint: disable=protected-access
    assert tool._stix_object is not None
    assert isinstance(tool._stix_object, StixTool)

@pytest.mark.usefixtures('clean_db')
def test_update_tool():
    """Tests that a Tool object is succesfully updated."""
    tool = Tool(
        name='asd', labels=['label1'], description='dsa', tool_version='1.0',
        kill_chain_phases=[
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'testing'},
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'debugging'}
        ]
    )
    tool.save()
    stix_id = tool.id
    updated = tool.update({'name': 'dsa'})
    assert updated.name == 'dsa'
    assert updated.id == stix_id
    assert updated.description == 'dsa'
    assert updated.tool_version == '1.0'
    assert updated.kill_chain_phases == [
        {'kill_chain_name': 'yeti-kc', 'phase_name': 'testing'},
        {'kill_chain_name': 'yeti-kc', 'phase_name': 'debugging'}
    ]
