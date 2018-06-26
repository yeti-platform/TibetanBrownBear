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
