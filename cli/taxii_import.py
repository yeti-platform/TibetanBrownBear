"""List and import TAXII collections into Yeti."""
import json

import click
from stix2 import TAXIICollectionSource, Filter
from taxii2client import Collection, Server

from yeti.core.entities import attack_pattern
from yeti.core.entities import campaign
from yeti.core.entities import course_of_action
from yeti.core.entities import identity
from yeti.core.entities import intrusion_set
from yeti.core.entities import malware
from yeti.core.entities import threat_actor
from yeti.core.entities import tool
from yeti.core.entities import vulnerability

# TODO: Change this to use the RESTful API instead of local DB commands.

def _get_collection_url(server_url):
    server = Server(server_url)
    api_root = server.api_roots[0]
    collections = list(api_root.collections)
    print('{0:s} has {1:d} collections: '.format(server_url, len(collections)))
    for index, collection in enumerate(collections):
        print("[{0:d}] {1:s}: {2:s}".format(index, collection.title, collection.id))

    collection_url = None
    while not collection_url:
        choice = input('Pick one: ')
        try:
            collection_url = collections[int(choice)].url
        except (ValueError, IndexError):
            print('Please specify a number from 0 to {0:d}'.format(len(collections)))

    return collection_url

@click.command()
@click.option('--collection_url', help='Remote TAXII collection URL ', type=click.STRING)  # pylint: disable=line-too-long
@click.option('--server_url', help='Remote TAXII collection URL ', type=click.STRING)  # pylint: disable=line-too-long
def taxii_import(server_url, collection_url):

    if not (server_url or collection_url):
        print('Please specify one of --server_url or --collection_url')
        exit(-1)

    if server_url:
        collection_url = _get_collection_url(server_url)

    if collection_url:
        print('Importing data from collection at: {0:s}'.format(collection_url))
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

            for item in tc_source.query(Filter('type', '=', name)):
                item_json = json.loads(item.serialize())
                obj = yeti_class.get(item.id)
                all_objects[item['id']] = obj

                if not obj:
                    obj = yeti_class(**item).save()
                    stats['new'] += 1
                    continue

                if obj.modified >= item.modified:
                    continue

                if obj.revoked:
                    stats['skipped'] += 1
                    continue

                if obj.equals(item_json):
                    stats['skipped'] += 1
                    continue

                obj.update(item_json)
                stats['updated'] += 1

            print('New: {0:d}, Updated: {1:d}, Skipped: {2:d}'.format(
                stats['new'], stats['updated'], stats['skipped']
            ))

        print('Getting relationships')
        stats = 0
        taxii_filter = Filter('type', '=', 'relationship')
        for relationship in tc_source.query(taxii_filter):
            stats += 1
            source = all_objects[relationship.source_ref]
            target = all_objects[relationship.target_ref]
            source.link_to(target, stix_rel=json.loads(
                relationship.serialize()))
        print('Added {0:d} relationships'.format(stats))
