export const editFields = {
  'attack-pattern': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ],
  'campaign': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'aliases', type: 'list'},
    {name: 'first_seen', type: 'datetime'},
    {name: 'last_seen', type: 'datetime'},
    {name: 'objective', type: 'text'}
  ],
  'course-of-action': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'description', type: 'longtext'}
  ],
  'identity': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'description', type: 'longtext'},
    {name: 'identity_class', type: 'text'},
    {name: 'sectors', type: 'list'},
    {name: 'contact_information', type: 'text'}
  ],
  'intrusion-set': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'description', type: 'longtext'},
    {name: 'aliases', type: 'list'},
    {name: 'first_seen', type: 'datetime'},
    {name: 'last_seen', type: 'datetime'},
    {name: 'goals', type: 'list'},
    {name: 'resource_level', type: 'text'},
    {name: 'primary_motivation', type: 'text'},
    {name: 'secondary_motivations', type: 'list'}
  ],
  'malware': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list', vocab: 'malware-label-ov'},
    {name: 'description', type: 'longtext'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ],
  'observed-data': [
    {name: 'id', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'first_observed', type: 'text'},
    {name: 'last_observed', type: 'text'},
    {name: 'number_observed', type: 'int'}
  ],
  'report': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'description', type: 'longtext'},
    {name: 'published', type: 'datetime'}
  ],
  'threat-actor': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'description', type: 'longtext'},
    {name: 'aliases', type: 'list'},
    {name: 'roles', type: 'list'},
    {name: 'goals', type: 'list'},
    {name: 'sophistication', type: 'text'},
    {name: 'resource_level', type: 'text'},
    {name: 'primary_motivation', type: 'text'},
    {name: 'secondary_motivations', type: 'list'},
    {name: 'personal_motivations', type: 'list'}
  ],
  'tool': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'description', type: 'longtext'},
    {name: 'tool_version', type: 'text'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ],
  'vulnerability': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'description', type: 'longtext'}
  ]
}

export const listFields = {
  'attack-pattern': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ],
  'campaign': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'aliases', type: 'list'},
    {name: 'first_seen', type: 'datetime'},
    {name: 'last_seen', type: 'datetime'}
  ],
  'course-of-action': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'}
  ],
  'identity': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'sectors', type: 'list'}
  ],
  'intrusion-set': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'aliases', type: 'list'},
    {name: 'first_seen', type: 'text'},
    {name: 'last_seen', type: 'text'},
    {name: 'primary_motivation', type: 'text'}
  ],
  'malware': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list', vocab: 'malware'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ],
  'observed-data': [
    {name: 'id', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'first_observed', type: 'text'},
    {name: 'last_observed', type: 'text'},
    {name: 'number_observed', type: 'int'}
  ],
  'report': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'published', type: 'datetime'}
  ],
  'threat-actor': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'aliases', type: 'list'},
    {name: 'roles', type: 'list'},
    {name: 'primary_motivation', type: 'text'}
  ],
  'tool': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'tool_version', type: 'text'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ],
  'vulnerability': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'}
  ]
}

export const defaultObjects = {
  'malware': {
    type: 'malware'
  },
  'threat-actor': {
    type: 'threat-actor'
  },
  'report': {
    type: 'report'
  },
  'attack-pattern': {
    type: 'attack-pattern'
  },
  'tool': {
    type: 'tool'
  },
  'intrusion-set': {
    type: 'intrusion-set'
  },
  'vulnerability': {
    type: 'vulnerability'
  },
  'campaign': {
    type: 'campaign'
  },
  'course-of-action': {
    type: 'course-of-action'
  },
  'identity': {
    type: 'identity'
  }
  // No definition for observed-data since we're not currently supporting
  // manual creation.
}
