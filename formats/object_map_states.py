from . import object_map as om

DEFAULT_STATES = ['added', 'removed', 'unchanged']


def create_empty(class_list=None, state_list=None):
    return {
        **om.create_empty(class_list), 'state_list':
        DEFAULT_STATES if state_list is None else state_list
    }


def create_empty_object(num_classes=None, num_states=None):
    return {
        **om.create_empty_object(num_classes), 'state_probs':
        [0] * (len(DEFAULT_STATES) if num_states is None else num_states)
    }


def validate(result):
    om.validate(result)
    for o, i in enumerate(result['objects']):
        om._validate_numbers_list(
            o['state_probs'],
            "The 'state_probs' field in object '%d' isn't a list of numbers "
            "with the same length as 'state_list' (%d))" %
            (i, len(result['state_probs'])), len(result['state_probs']))
    assert ('state_probs' in result and type(result['state_probs'] == list)
            and all(type(x) == str for x in result['state_probs'])), \
            "Object maps with states must contain a state_list (list of strings)"
