"""Library of Python functions to interact with Yeti's RESTful API."""

import base64

import requests
from stix2 import Relationship

from yeti.core.indicators import indicator, regex, yara, indicator_base

from yeti.core.entities import attack_pattern
from yeti.core.entities import campaign
from yeti.core.entities import course_of_action
from yeti.core.entities import identity
from yeti.core.entities import intrusion_set
from yeti.core.entities import malware
from yeti.core.entities import threat_actor
from yeti.core.entities import tool
from yeti.core.entities import vulnerability
from yeti.core.entities import entity

API_BASE = 'http://localhost:5000/api/'
TYPES_DICT = {
    obj.type: obj
    for obj in [
        indicator.Indicator,
        regex.Regex,
        yara.Yara,
        attack_pattern.AttackPattern,
        campaign.Campaign,
        course_of_action.CourseOfAction,
        identity.Identity,
        intrusion_set.IntrusionSet,
        malware.Malware,
        threat_actor.ThreatActor,
        tool.Tool,
        vulnerability.Vulnerability,
    ]
}

class YetiAPI:

    def __init__(self, api_base, api_key):
        self.api_base = api_base
        self.api_key = api_key

    def filter_entities(self, name, entity_type):
        """Fetches Entities based on name and entity type.

        Args:
            name: String to filter the name on
            entity_type: String, Entity type (STIX 2 native or extended type).

        Returns:
            A list of Yeti Entities.
        """
        data = {'name': name, 'type': entity_type}
        yeti_objects = []
        for item in self._do_post('entities/filter/', data):
            yeti_objects.append(TYPES_DICT[item['type']](**item))
        return yeti_objects

    def filter_indicators(self, name, indicator_type):
        """Fetches Indicators based on name and indicator type.

        Args:
            name: String to filter the name on
            indicator_type: String, Indicator type (STIX 2 native or extended type).

        Returns:
            A list of Yeti Indicators.
        """
        data = {'name': name, 'type': indicator_type}
        yeti_objects = []
        for item in self._do_post('indicators/filter/', data):
            yeti_objects.append(TYPES_DICT[item['type']](**item))
        return yeti_objects

    def get_neighbors(self, obj):
        """Fethes neighbors for a Yeti object.

        Args:
        obj: Yeti object to fetch neighbors for.

        Returns:
            A dictionary containing a list of STIX 2 Relationships (in the 'edge'
                key) and a `{id: object}` dictionary of Yeti objects (in the
                'vertices' key).
        """
        if isinstance(obj, entity.Entity):
            uri = 'entities/{0:s}/neighbors/'.format(obj.id)
        if isinstance(obj, indicator_base.Indicator):
            uri = 'indicators/{0:s}/neighbors/'.format(obj.id)
        response = self._do_post(uri, data={})
        response['edges'] = [Relationship(**r) for r in response['edges']]
        vertices = []
        for item in response['vertices']:
            vertices.append(TYPES_DICT[item['type']](**item))
        response['vertices'] = vertices
        return response

    def _do_post(self, endpoint, data):
        """Performs a POST request to the Yeti webserver.

        Args:
            endpoint: endpoint suffix.
            data: a JSON dict to be sent with the request.

        Returns:
            A dictionary representing the decoded JSON response.
        """
        response = requests.post(
            self.api_base + endpoint,
            json=data,
            headers={'X-Yeti-API': self.api_key})
        if response.status_code != 200:
            print('Error: {0:d}'.format(response.status_code))
            print(response.json())
            exit(-1)
        return response.json()

    def _do_get(self, endpoint):
        """Performs a GET request to the Yeti webserver.

        Args:
            endpoint: endpoint suffix.

        Returns:
            A dictionary representing the decoded JSON response.
        """
        response = requests.get(
            self.api_base + endpoint,
            headers={'X-Yeti-API': self.api_key})
        if response.status_code != 200:
            print('Error: {0:d}'.format(response.status_code))
            print(response.json())
            exit(-1)
        return response.json()

    def match_data(self, data):
        """Matches data against Yeti's indicators.

        Args:
            data: (str, binary) The data to match against Yeti.

        Returns:
            A dictionary representing the decoded JSON list of matches.
        """
        if isinstance(data, str):
            payload = [{'encoding': 'utf-8', 'data': data.encode('utf-8')}]
        else:
            payload = [{'encoding': 'b64', 'data': base64.b64encode(data)}]
        return self._do_post('indicators/match/', payload)
