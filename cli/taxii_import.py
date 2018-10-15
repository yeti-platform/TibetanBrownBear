#!/usr/bin/env
import click
from stix2 import TAXIICollectionSource, Filter
from taxii2client import Collection

from yeti.core.entities import attack_pattern
from yeti.core.entities import campaign
from yeti.core.entities import course_of_action
from yeti.core.entities import identity
from yeti.core.entities import intrusion_set
from yeti.core.entities import malware
from yeti.core.entities import threat_actor
from yeti.core.entities import tool
from yeti.core.entities import vulnerability

@click.command()
@click.option('--collection_url', help='Remote TAXII collection URL ', type=click.STRING, required=True)  # pylint: disable=line-too-long
def taxii_import(collection_url):
    print('Importing data from collection at: {0:s}')
    collection = Collection(collection_url)
    tc_source = TAXIICollectionSource(collection)

    object_classes = {
        'attack-pattern': attack_pattern.AttackPattern,
        'campaign': campaign.Campaign,
        'course-of-action': course_of_action.CourseOfAction,
        'identity': identity.Identity,
        'intrusion-set': intrusion_set.IntrusionSet,
        'malware': malware.Malware,
        'threat-actor': threat_actor.ThreatActor,
        'tool': tool.Tool,
        'vulnerability': vulnerability.Vulnerability,
    }

    all_objects = {}

    for name, yeti_class in object_classes.items():
        print('Fetching', name)
        stats = {
            'updated': 0,
            'new': 0,
            'skipped': 0,
        }

        items = tc_source.query(Filter('type', '=', name))
        for item in items:
            obj = yeti_class.find(stix_id=item['id'])
            if not obj:
                obj = yeti_class.from_stix_object(item).save()
                stats['new'] += 1
            elif obj.equals(item):
                stats['skipped'] += 1
            else:
                obj.update(item)
                stats['updated'] += 1
            all_objects[item['id']] = obj

        print('New: {0:d}, Updated: {1:d}, Skipped: {2:d}'.format(
            stats['new'], stats['updated'], stats['skipped']
        ))

    print('Getting relationships')
    stats = 0
    for relationship in tc_source.query(Filter('type', '=', 'relationship')):
        stats += 1
        source = all_objects[relationship.source_ref]
        target = all_objects[relationship.target_ref]
        source.link_to(target, stix_rel=relationship.serialize())
    print('Added {0:d} relationships'.format(stats))
