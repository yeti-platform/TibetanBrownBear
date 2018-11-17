"""Tests for the Stix2 bindings."""

from stix2 import Relationship as StixRelationship
from yeti.core.relationships.relationship import Relationship


def test_relationship_creation(populate_malware):
    """Tests the creation of a single Relationship object."""
    relationship = Relationship(
        attributes={
            'source_ref': populate_malware[0].id,
            'target_ref': populate_malware[1].id,
            'relationship_type': 'related-to'
        },
        db_from=populate_malware[0].id,
        db_to=populate_malware[1].id,
    )
    # pylint: disable=protected-access
    assert relationship._stix_object is not None
    assert isinstance(relationship._stix_object, StixRelationship)
