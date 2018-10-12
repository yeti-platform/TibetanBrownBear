export const editFields = {
  'indicator': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'description', type: 'longtext'},
    {name: 'pattern', type: 'code'},
    {name: 'valid_from', type: 'datetime'},
    {name: 'valid_until', type: 'datetime'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ],
  'x-regex': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'description', type: 'longtext'},
    {name: 'pattern', type: 'code'},
    {name: 'valid_from', type: 'datetime'},
    {name: 'valid_until', type: 'datetime'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ]
}

export const listFields = {
  'indicator': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ],
  'x-regex': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'kill_chain_phases', type: 'killchain'}
  ]
}

export const defaultObjects = {
  'indicator': {
    type: 'indicator'
  },
  'regex': {
    type: 'x-regex'
  }
}
