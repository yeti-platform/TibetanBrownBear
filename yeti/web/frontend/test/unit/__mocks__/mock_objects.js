const mockMalware = {
  _id: 'entities/510808',
  family: [
    'trojan',
    'banker'
  ],
  id: 510808,
  name: 'MyMalware',
  type: 'entity.malware'
}

const mockRegex = {
  _id: 'indicators/477775',
  id: 477775,
  name: 'MyIndicator',
  pattern: '[a-z]{1,2}',
  type: 'indicator.regex'
}

const mockHostname = {
  _id: 'observables/483373',
  id: 483373,
  idna: 'toto512.com',
  tags: [
    {
      expiration: '2018-05-02T15:39:06.543454+00:00',
      first_seen: '2018-05-01T15:39:06.543454+00:00',
      fresh: true,
      last_seen: '2018-05-01T17:15:16.567785+00:00',
      name: 'asd'
    },
    {
      expiration: '2018-05-02T16:50:52.002557+00:00',
      first_seen: '2018-05-01T16:50:52.002557+00:00',
      fresh: true,
      last_seen: '2018-05-01T17:15:16.567785+00:00',
      name: 'zxc'
    },
    {
      expiration: '2018-05-02T17:15:12.656922+00:00',
      first_seen: '2018-05-01T17:15:12.656922+00:00',
      fresh: true,
      last_seen: '2018-05-01T17:15:16.567785+00:00',
      name: 'qwe'
    }
  ],
  type: 'observable.hostname',
  value: 'toto512.com'
}

const mockObservableMatchresult = [
  {
    error: null,
    found: false,
    query: 'tota.com'
  },
  {
    error: null,
    found: [
      {
        _id: 'observables/1279581',
        id: 1279581,
        idna: 'toto.com',
        tags: null,
        type: 'observable.hostname',
        value: 'toto.com'
      }
    ],
    query: 'toto.com'
  },
  {
    error: 'Invalid observable type',
    found: false,
    query: 'asd'
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

module.exports.mockMalware = mockMalware
module.exports.mockRegex = mockRegex
module.exports.mockHostname = mockHostname
module.exports.mockObservableMatchresult = mockObservableMatchresult
module.exports.mockTagList = mockTagList
module.exports.mockMalwareList = [
  {
    _id: 'entities/1',
    family: [
      'trojan',
      'banker'
    ],
    id: 1,
    name: 'FirstMalware',
    type: 'entity.malware'
  },
  {
    _id: 'entities/2',
    family: [
      'keylogger'
    ],
    id: 2,
    name: 'SecondMalware',
    type: 'entity.malware'
  },
  {
    _id: 'entities/3',
    family: [],
    id: 3,
    name: 'ThirdMalware',
    type: 'entity.malware'
  }
]
