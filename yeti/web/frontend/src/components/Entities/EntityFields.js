export const editFields = {
  'attack-pattern': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stage'}
  ],
  'campaign': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'aliases', type: 'list', humanName: 'Aliases'},
    {name: 'first_seen', type: 'datetime', humanName: 'First seen'},
    {name: 'last_seen', type: 'datetime', humanName: 'Last seen'},
    {name: 'objective', type: 'text', humanName: 'Objective'}
  ],
  'course-of-action': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'description', type: 'longtext', humanName: 'Description'}
  ],
  'identity': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'identity_class', type: 'text', vocab: 'identity-class-ov', humanName: 'Identity class'},
    {name: 'sectors', type: 'list', vocab: 'industry-sector-ov', humanName: 'Industry sector'},
    {name: 'contact_information', type: 'text', humanName: 'Contact information'}
  ],
  'intrusion-set': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'aliases', type: 'list', humanName: 'Aliases'},
    {name: 'first_seen', type: 'datetime', humanName: 'First seen'},
    {name: 'last_seen', type: 'datetime', humanName: 'Last seen'},
    {name: 'goals', type: 'list', humanName: 'Goals'},
    {name: 'resource_level', type: 'text', vocab: 'attack-resource-level-ov'},
    {name: 'primary_motivation', type: 'text', vocab: 'attack-motivation-ov'},
    {name: 'secondary_motivations', type: 'list', vocab: 'attack-motivation-ov'}
  ],
  'malware': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', vocab: 'malware-label-ov'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stage'}
  ],
  'observed-data': [
    {name: 'id', type: 'text'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'first_observed', type: 'text'},
    {name: 'last_observed', type: 'text'},
    {name: 'number_observed', type: 'int'}
  ],
  'report': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', vocab: 'report-label-ov'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'published', type: 'datetime'}
  ],
  'threat-actor': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', vocab: 'threat-actor-label-ov'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'aliases', type: 'list', humanName: 'Aliases'},
    {name: 'roles', type: 'list', vocab: 'threat-actor-role-ov', humanName: 'Roles'},
    {name: 'goals', type: 'list', humanName: 'Goals'},
    {name: 'sophistication', type: 'text', vocab: 'threat-actor-sophistication-ov', humanName: 'Sophistication'},
    {name: 'resource_level', type: 'text', vocab: 'attack-resource-level-ov', humanName: 'Resource level'},
    {name: 'primary_motivation', type: 'text', vocab: 'attack-motivation-ov', humanName: 'Primary motivation'},
    {name: 'secondary_motivations', type: 'list', vocab: 'attack-motivation-ov', humanName: 'Secondary motivations'},
    {name: 'personal_motivations', type: 'list', vocab: 'attack-motivation-ov', humanName: 'Personal motivations'}
  ],
  'tool': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', vocab: 'tool-label-ov'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'tool_version', type: 'text', humanName: 'Tool version'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stage'}
  ],
  'vulnerability': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'description', type: 'longtext', humanName: 'Description'}
  ]
}

export const listFields = {
  'attack-pattern': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stage'}
  ],
  'campaign': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'aliases', type: 'list', humanName: 'Aliases'},
    {name: 'first_seen', type: 'datetime', humanName: 'First seen'},
    {name: 'last_seen', type: 'datetime', humanName: 'Last seen'}
  ],
  'course-of-action': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'}
  ],
  'identity': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'sectors', type: 'list', humanName: 'Sectors'}
  ],
  'intrusion-set': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'aliases', type: 'list', humanName: 'Aliases'},
    {name: 'first_seen', type: 'text', humanName: 'First seen'},
    {name: 'last_seen', type: 'text', humanName: 'Last seen'},
    {name: 'primary_motivation', type: 'text', humanName: 'Primary motivation'}
  ],
  'malware': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', vocab: 'malware-label-ov', humanName: 'Labels'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stage'}
  ],
  'observed-data': [
    {name: 'id', type: 'text', humanName: 'ID'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'first_observed', type: 'text', humanName: 'First observed'},
    {name: 'last_observed', type: 'text', humanName: 'last observed'},
    {name: 'number_observed', type: 'int', humanName: 'Number observed'}
  ],
  'report': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'published', type: 'datetime', humanName: 'Date published'}
  ],
  'threat-actor': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'aliases', type: 'list', humanName: 'Aliases'},
    {name: 'roles', type: 'list', humanName: 'Roles'},
    {name: 'primary_motivation', type: 'text', humanName: 'Primary motivation'}
  ],
  'tool': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'tool_version', type: 'text', humanName: 'Tool version'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stage'}
  ],
  'vulnerability': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'}
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
