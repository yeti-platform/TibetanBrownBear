from .types.observable import Observable

def match_observables(observables):
    """Matches a list of observables against the Yeti database."""
    normalized = []
    for observable in observables:
        result_item = {'query': observable}
        guessed_type = Observable.guess_type(observable)
        if not guessed_type:
            result_item['error'] = 'Invalid observable type'
            result_item['found'] = False
        else:
            observable_obj = guessed_type(value=observable)
            existing = Observable.filter({'value':observable_obj.value})
            if existing:
                result_item['found'] = [item.dump() for item in existing]
            else:
                result_item['found'] = False
            result_item['error'] = None
        normalized.append(result_item)
    return normalized
