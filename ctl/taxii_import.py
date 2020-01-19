"""List and import TAXII collections into Yeti."""
import json

import click
import requests
from stix2 import TAXIICollectionSource, Filter, datastore
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


OBJECT_CLASSES = {
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

def _lazy_get_object(all_objects, stix_id):
    if stix_id in all_objects:
        return all_objects[stix_id]
    for name, yeti_class in OBJECT_CLASSES.items():
        if stix_id.startswith(name):
            obj = yeti_class.get(stix_id)
            if not obj:
                raise RuntimeError('No data found for STIX ID: {0:s}'.format(stix_id))
            return obj

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
@click.option('--server_url', help='Remote TAXII server URL ', type=click.STRING)  # pylint: disable=line-too-long
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

        all_objects = {}

        for name, yeti_class in OBJECT_CLASSES.items():
            print('Fetching', name)
            stats = {
                'updated': 0,
                'new': 0,
                'skipped': 0,
            }

            try:
                for item in tc_source.query(Filter('type', '=', name)):
                    item_json = json.loads(item.serialize())
                    obj = yeti_class.get(item.id)

                    if not obj:
                        obj = yeti_class(**item).save()
                        stats['new'] += 1
                    elif obj.modified >= item.modified or obj.revoked or obj.equals(item_json):
                        stats['skipped'] += 1
                    elif obj.modified < item.modified:
                        obj.update(item_json)
                        stats['updated'] += 1

                    all_objects[item['id']] = obj

            except requests.exceptions.HTTPError as error:
                print(f'HTTPError: {error}')
            except datastore.DataSourceError as error:
                print(f'DataSourceError: {error}')

            print(f"[{name}] New: {stats['new']}, Updated: {stats['updated']}, "
                  f"Skipped: {stats['skipped']}")

        print('Getting relationships')
        stats = 0
        taxii_filter = Filter('type', '=', 'relationship')
        for relationship in tc_source.query(taxii_filter):
            stats += 1
            source = _lazy_get_object(all_objects, relationship.source_ref)
            target = _lazy_get_object(all_objects, relationship.target_ref)
            source.link_to(target, stix_rel=json.loads(
                relationship.serialize()))
        print('Added {0:d} relationships'.format(stats))
