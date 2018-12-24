export const editFields = {
  'indicator': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'pattern', type: 'code', humanName: 'STIX pattern'},
    {name: 'valid_from', type: 'datetime', humanName: 'Valid from'},
    {name: 'valid_until', type: 'datetime', humanName: 'Valid until'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stages'}
  ],
  'x-regex': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'pattern', type: 'code', humanName: 'Regular expression'},
    {name: 'valid_from', type: 'datetime', humanName: 'Valid from'},
    {name: 'valid_until', type: 'datetime', humanName: 'Valid until'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stages'}
  ],
  'x-yara': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'pattern', type: 'code', humanName: 'Yara rule'},
    {name: 'valid_from', type: 'datetime', humanName: 'Valid from'},
    {name: 'valid_until', type: 'datetime', humanName: 'Valid until'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stages'}
  ],
  'x-sigma': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'description', type: 'longtext', humanName: 'Description'},
    {name: 'pattern', type: 'code', humanName: 'Sigma rule'},
    {name: 'valid_from', type: 'datetime', humanName: 'Valid from'},
    {name: 'valid_until', type: 'datetime', humanName: 'Valid until'}
  ]
}

export const listFields = {
  'indicator': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stages'}
  ],
  'x-regex': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stages'}
  ],
  'x-yara': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stages'}
  ],
  'x-sigma': [
    {name: 'name', type: 'text', humanName: 'Name'},
    {name: 'labels', type: 'list', humanName: 'Labels'},
    {name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stages'}
  ]
}

export const defaultObjects = {
  'indicator': {
    type: 'indicator'
  },
  'x-regex': {
    type: 'x-regex'
  },
  'x-yara': {
    type: 'x-yara'
  },
  'x-sigma': {
    type: 'x-sigma'
  }
}
