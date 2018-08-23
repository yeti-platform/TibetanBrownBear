"""Tests for the Stix2 bindings."""

import pytest

from yeti.core.errors import ValidationError
from yeti.core.entities.attack_pattern import AttackPattern
from stix2 import AttackPattern as StixAttackPattern

@pytest.mark.usefixtures('clean_db')
def test_attack_pattern_creation():
    """Tests the creation of a single AttackPattern object."""
    attack_pattern = AttackPattern(
        name='asd', labels=['label1'], kill_chain_phases=[
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'testing'},
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'debugging'}
        ]
    )
    # pylint: disable=protected-access
    assert attack_pattern._stix_object is not None
    assert isinstance(attack_pattern._stix_object, StixAttackPattern)

@pytest.mark.usefixtures('clean_db')
def test_update_attack_pattern():
    """Tests that a AttackPattern object is succesfully updated."""
    attack_pattern = AttackPattern(
        name='asd', labels=['label1'], description='dsa', kill_chain_phases=[
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'testing'},
            {'kill_chain_name': 'yeti-kc', 'phase_name': 'debugging'}
        ]
    )
    attack_pattern.save()
    stix_id = attack_pattern.id
    updated = attack_pattern.update({'name': 'dsa'})
    assert updated.name == 'dsa'
    assert updated.id == stix_id
    assert updated.description == 'dsa'
    assert updated.kill_chain_phases == [
        {'kill_chain_name': 'yeti-kc', 'phase_name': 'testing'},
        {'kill_chain_name': 'yeti-kc', 'phase_name': 'debugging'}
    ]
