export const relationships = {
  'attack-pattern': {
    'identity': ['targets'],
    'vulnerability': ['targets'],
    'malware': ['uses'],
    'tool': ['uses']
  },
  'campaign': {
    'intrusion-set': ['attributed-to'],
    'threat-actor': ['attributed-to'],
    'identity': ['targets'],
    'vulnerabiliyt': ['targets'],
    'attack-pattern': ['uses'],
    'malware': ['uses'],
    'tool': ['uses']
  },
  'course-of-action': {
    'attack-pattern': ['mitigates'],
    'malware': ['mitigates'],
    'tool': ['mitigates'],
    'vulnerability': ['mitigates']
  },
  'identity': { },
  'indicator': {
    'attack-pattern': ['indicates'],
    'campaign': ['indicates'],
    'intrusion-set': ['indicates'],
    'malware': ['indicates'],
    'threat-actor': ['indicates'],
    'tool': ['indicates']
  },
  'intrusion-set': {
    'threat-actor': ['attributed-to'],
    'identity': ['targets'],
    'vulnerabiliyt': ['targets'],
    'attack-pattern': ['uses'],
    'malware': ['uses'],
    'tool': ['uses']
  },
  'malware': {
    'identity': ['targets'],
    'vulnerability': ['targets'],
    'uses': ['tool'],
    'malware': ['variant-of']
  },
  'observed-data': { },
  'report': { },
  'threat-actor': {
    'identity': ['attributed-to', 'impersonates', 'targets'],
    'vulnerability': ['targets'],
    'attack-pattern': ['uses'],
    'malware': ['uses'],
    'tool': ['uses']
  },
  'tool': {
    'identity': ['targets'],
    'vulnerability': ['targets']
  }
}

// STIX extensions:

relationships['x-regex'] = relationships['indicator']
relationships['x-yara'] = relationships['indicator']
