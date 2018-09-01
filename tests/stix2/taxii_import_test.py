import pytest

from stix2 import Malware as StixMalware

from yeti.core.entities.malware import Malware

# pylint: disable=line-too-long
MITRE_MALWARE = StixMalware(**{
    'allow_custom': True,
    'type': 'malware',
    'id': 'malware--79499993-a8d6-45eb-b343-bf58dea5bdde',
    'created_by_ref': 'identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5',
    'created': '2018-04-18T17:59:24.739Z',
    'modified': '2018-04-18T17:59:24.739Z',
    'name': 'Briba',
    'description': 'Briba is a trojan used by Elderwood to open a backdoor and download files on to compromised hosts. (Citation: Symantec Elderwood Sept 2012) (Citation: Symantec Briba May 2012)\n\nAliases: Briba',
    'labels': [
        'malware'
    ],
    'external_references': [
        {
            'source_name': 'mitre-attack',
            'url': 'https://attack.mitre.org/wiki/Software/S0204',
            'external_id': 'S0204'
        },
        {
            'source_name': 'Symantec Elderwood Sept 2012',
            'description': 'O\'Gorman, G., and McDonald, G.. (2012, September 6). The Elderwood Project. Retrieved February 15, 2018.',
            'url': 'http://www.symantec.com/content/en/us/enterprise/media/security%20response/whitepapers/the-elderwood-project.pdf'
        },
        {
            'source_name': 'Symantec Briba May 2012',
            'description': 'Ladley, F. (2012, May 15). Backdoor.Briba. Retrieved February 21, 2018.',
            'url': 'https://www.symantec.com/security%20response/writeup.jsp?docid=2012-051515-2843-99'
        }
    ],
    'object_marking_refs': [
        'marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168'
    ],
    'x_mitre_aliases': [
        'Briba'
    ]
})


@pytest.mark.usefixtures('clean_db')
def test_malware_import():
    """Tests the importing the result of MTIRE's TAXII information."""
    malware = Malware.from_stix_object(MITRE_MALWARE).save()
    # pylint: disable=protected-access
    assert malware._stix_object is not None
    assert isinstance(malware._stix_object, StixMalware)
    assert malware.type == 'malware'
    assert malware.id == 'malware--79499993-a8d6-45eb-b343-bf58dea5bdde'
    assert malware.created_by_ref == 'identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5'
    assert str(malware.created) == '2018-04-18 17:59:24.739000+00:00'
    assert str(malware.modified) == '2018-04-18 17:59:24.739000+00:00'
    assert malware.name == 'Briba'
    assert malware.description == 'Briba is a trojan used by Elderwood to open a backdoor and download files on to compromised hosts. (Citation: Symantec Elderwood Sept 2012) (Citation: Symantec Briba May 2012)\n\nAliases: Briba'
    assert malware.labels == ['malware']
    assert malware.external_references == [
        {
            'source_name': 'mitre-attack',
            'url': 'https://attack.mitre.org/wiki/Software/S0204',
            'external_id': 'S0204'
        },
        {
            'source_name': 'Symantec Elderwood Sept 2012',
            'description': 'O\'Gorman, G., and McDonald, G.. (2012, September 6). The Elderwood Project. Retrieved February 15, 2018.',
            'url': 'http://www.symantec.com/content/en/us/enterprise/media/security%20response/whitepapers/the-elderwood-project.pdf'
        },
        {
            'source_name': 'Symantec Briba May 2012',
            'description': 'Ladley, F. (2012, May 15). Backdoor.Briba. Retrieved February 21, 2018.',
            'url': 'https://www.symantec.com/security%20response/writeup.jsp?docid=2012-051515-2843-99'
        }
    ]
    assert malware.object_marking_refs == ['marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168']
    assert malware.get_extended_property('x_mitre_aliases') == ['Briba']
