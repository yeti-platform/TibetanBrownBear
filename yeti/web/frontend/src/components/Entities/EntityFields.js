export const typeFields = {
  'malware': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list', autocompleteValues: ['trojan', 'banker']}
  ],
  'threat-actor': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'}
  ],
  'attack-pattern': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'}
  ],
  'tool': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'tool_version', type: 'text'}
  ],
  'intrusion-set': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'first_seen', type: 'text'},
    {name: 'last_seen', type: 'text'}
  ],
  'vulnerability': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'}
  ],
  'campaign': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'first_seen', type: 'text'},
    {name: 'last_seen', type: 'text'},
    {name: 'objective', type: 'text'}
  ],
  'course-of-action': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'}
  ],
  'identity': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'identity_class', type: 'text'},
    {name: 'sectors', type: 'list'},
    {name: 'contact_information', type: 'text'}
  ]
}

export const defaultObjects = {
  'malware': {
    type: 'malware',
    labels: []
  },
  'threat-actor': {
    type: 'threat-actor',
    labels: []
  },
  'attack-pattern': {
    type: 'attack-pattern',
    labels: []
  },
  'tool': {
    type: 'tool',
    labels: []
  },
  'intrusion-set': {
    type: 'intrusion-set',
    labels: []
  },
  'vulnerability': {
    type: 'vulnerability',
    labels: []
  },
  'campaign': {
    type: 'campaign',
    labels: []
  },
  'course-of-action': {
    type: 'course-of-action',
    labels: []
  },
  'identity': {
    type: 'identity',
    labels: []
  }
}
