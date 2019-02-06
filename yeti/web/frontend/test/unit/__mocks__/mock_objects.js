const mockKillChains = [
  {
    'description': 'KC1 description',
    'human_name': 'KC1',
    'id': 12345,
    'name': 'kc1',
    'settings': {
      'kc1': [
        {
          'description': 'First and last phase',
          'name': 'foo'
        }
      ]
    }
  }
]

const mockNeighbors = {
  'edges': [
    {
      'created': '2017-05-31T21:33:27.034Z',
      'created_by_ref': 'identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5',
      'id': 'relationship--d242dc5a-3969-498c-b7eb-5d850e7d384d',
      'modified': '2018-10-17T00:14:20.652Z',
      'object_marking_refs': [
        'marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168'
      ],
      'relationship_type': 'uses',
      'source_ref': 'intrusion-set--c47f937f-1022-4f42-8525-e7a4779a14cb',
      'target_ref': 'malware1',
      'type': 'relationship'
    },
    {
      'created': '2017-05-31T21:33:27.034Z',
      'created_by_ref': 'identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5',
      'id': 'relationship--762f85a3-0120-4b09-aafd-3f460764e85f',
      'modified': '2018-10-17T00:14:20.652Z',
      'object_marking_refs': [
        'marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168'
      ],
      'relationship_type': 'uses',
      'source_ref': 'intrusion-set--c47f937f-1022-4f42-8525-e7a4779a14cb',
      'target_ref': 'malware2',
      'type': 'relationship'
    }
  ],
  'vertices': {
    'attackpattern1': {
      'created': '2017-05-31T21:30:19.735Z',
      'created_by_ref': 'identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5',
      'description': 'blah',
      'external_references': [],
      'id': 'attackpattern1',
      'kill_chain_phases': [
        {
          'kill_chain_name': 'kc1',
          'phase_name': 'foo'
        }
      ],
      'modified': '2018-10-17T00:14:20.652Z',
      'name': 'Credential Dumping',
      'object_marking_refs': [
        'marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168'
      ],
      'type': 'attack-pattern'
    },
    'malware1': {
      'created': '2017-05-31T21:32:11.911Z',
      'created_by_ref': 'identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5',
      'description': '[RIPTIDE](https://attack.mitre.org/software/S0003) is a proxy-aware backdoor used by [APT12](https://attack.mitre.org/groups/G0005). (Citation: Moran 2014)',
      'external_references': [
        {
          'external_id': 'S0003',
          'source_name': 'mitre-attack',
          'url': 'https://attack.mitre.org/software/S0003'
        },
        {
          'description': 'Moran, N., Oppenheim, M., Engle, S., & Wartell, R.. (2014, September 3). Darwin\u2019s Favorite APT Group &#91;Blog&#93;. Retrieved November 12, 2014.',
          'source_name': 'Moran 2014',
          'url': 'https://www.fireeye.com/blog/threat-research/2014/09/darwins-favorite-apt-group-2.html'
        }
      ],
      'id': 'malware1',
      'labels': [
        'malware'
      ],
      'modified': '2018-10-17T00:14:20.652Z',
      'name': 'RIPTIDE',
      'object_marking_refs': [
        'marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168'
      ],
      'type': 'malware',
      'x_mitre_aliases': [
        'RIPTIDE'
      ],
      'x_mitre_platforms': [
        'Windows'
      ],
      'x_mitre_version': '1.0'
    }
  }
}

const mockMalware = {
  created: '2018-06-26T20:16:05.914Z',
  id: 'malware--976c0bcf-91f3-4ab8-a0cf-f01692afcb5b',
  labels: [
    'trojan', 'banker'
  ],
  modified: '2018-06-26T20:16:05.914Z',
  name: 'Gootkit',
  type: 'malware'
}

const mockVocabs = {
  'malware-label-ov': [
    'adware',
    'backdoor',
    'bot',
    'ddos',
    'dropper',
    'exploit-kit',
    'keylogger',
    'ransomware',
    'remote-access-trojan',
    'resource-exploitation',
    'rogue-security-software',
    'rootkit',
    'screen-capture',
    'spyware',
    'trojan',
    'virus',
    'worm'
  ]
}

const mockHostname = {
  'id': 2685155,
  'type': 'domain-name',
  'value': 'tomchop.me'
}

const mockObservableMatchresult = [
  {
    'error': null,
    'found': [
      {
        'id': 2685155,
        'type': 'domain-name',
        'value': 'tomchop.me'
      }
    ],
    'query': 'tomchop.me'
  },
  {
    'error': 'Invalid observable type',
    'found': false,
    'query': 'asd'
  },
  {
    'error': null,
    'found': false,
    'query': 'tota.com'
  }
]

const mockTagList = [
  {
    _id: 'tags/2047185',
    created_at: '2018-06-05T20:06:35.945646+00:00',
    default_expiration: '6400',
    id: '2047185',
    name: 'mytag',
    selected: false
  }, {
    _id: 'tags/2047186',
    created_at: '2018-06-05T20:06:35.945646+00:00',
    default_expiration: '6400',
    id: '2047186',
    name: 'mytag2',
    selected: false
  }, {
    _id: 'tags/2047187',
    created_at: '2018-06-05T20:06:35.945646+00:00',
    default_expiration: '6400',
    id: '2047187',
    name: 'mytag3',
    selected: false
  }
]

const mockAsyncJobList = [
  {
    _id: 'asyncjobsettings/1400943',
    enabled: true,
    id: 1400943,
    last_executed: '2018-05-27T11:10:31.803160+00:00',
    name: 'FakeFeed1',
    period: 86400.0,
    status: 'idle'
  }, {
    _id: 'asyncjobsettings/1400944',
    enabled: true,
    id: 1400944,
    last_executed: '2018-05-27T11:10:31.803160+00:00',
    name: 'FakeFeed2',
    period: 86400.0,
    status: 'idle'
  }, {
    _id: 'asyncjobsettings/1400945',
    enabled: true,
    id: 1400945,
    last_executed: '2018-05-27T11:10:31.803160+00:00',
    name: 'FakeFeed3',
    period: 86400.0,
    status: 'idle'
  }
]

module.exports.mockNeighbors = mockNeighbors
module.exports.mockKillChains = mockKillChains
module.exports.mockVocabs = mockVocabs
module.exports.mockMalware = mockMalware
module.exports.mockHostname = mockHostname
module.exports.mockObservableMatchresult = mockObservableMatchresult
module.exports.mockTagList = mockTagList
module.exports.mockAsyncJobList = mockAsyncJobList
module.exports.mockMalwareList = [
  {
    created: '2018-06-26T20:16:05.914Z',
    id: 'malware--976c0bcf-0000-4ab8-a0cf-f01692afcb5b',
    labels: [
      'trojan'
    ],
    modified: '2018-06-26T20:16:05.914Z',
    name: 'Gootkit',
    type: 'malware'
  },
  {
    created: '2018-06-26T20:16:05.914Z',
    id: 'malware--976c0bcf-1111-4ab8-a0cf-f01692afcb6b',
    labels: [
      'apt'
    ],
    modified: '2018-06-26T20:16:05.914Z',
    name: 'Sofacy',
    type: 'malware'
  },
  {
    created: '2018-06-26T20:16:05.914Z',
    id: 'malware--976c0bcf-2222-4ab8-a0cf-f01692afcb5b',
    labels: [
      'china'
    ],
    modified: '2018-06-26T20:16:05.914Z',
    name: 'Plugx',
    type: 'malware'
  }
]
