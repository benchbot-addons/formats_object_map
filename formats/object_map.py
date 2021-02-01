import numbers

DEFAULT_CLASS_LIST = [
    'bottle', 'cup', 'knife', 'bowl', 'wine glass', 'fork', 'spoon', 'banana',
    'apple', 'orange', 'cake', 'potted plant', 'mouse', 'keyboard', 'laptop',
    'cell phone', 'book', 'clock', 'chair', 'table', 'couch', 'bed', 'toilet',
    'tv', 'microwave', 'toaster', 'refrigerator', 'oven', 'sink', 'person',
    'background'
]


def create_empty(class_list=None):
    return {
        'objects': [],
        'class_list': DEFAULT_CLASS_LIST if class_list is None else class_list
    }


def create_empty_object(num_classes=None):
    return {
        'label_probs': [0] *
        (len(DEFAULT_CLASS_LIST) if num_classes is None else num_classes),
        'centroid': [0] * 3,
        'extent': [0] * 3
    }


def _validate_numbers_list(value, msg, required_length=None):
    assert (type(value) == list
            and all(isinstance(x, numbers.Number) for x in value) and
            (required_length == None or len(value) == required_length)), msg


def validate(result):
    assert ('objects' in result and type(result['objects'] == list)
            ), "Object maps must contain a list of objects"
    for i, o in enumerate(result['objects']):
        _validate_numbers_list(
            o['label_probs'],
            "The 'label_probs' field in object '%d' isn't a list of numbers "
            "with the same length as 'class_list' (%d)" %
            (i, len(result['class_list'])), len(result['class_list']))
        _validate_numbers_list(
            o['centroid'],
            "The 'centroid' field in object '%d' isn't a list of numbers "
            "with a length of 3" % i, 3)
        _validate_numbers_list(
            o['extent'],
            "The 'centroid' field in object '%d' isn't a list of numbers "
            "with a length of 3" % i, 3)
    assert (
        'class_list' in result and type(result['class_list']) == list
        and result['class_list']
        and all(type(x) == str for x in result['class_list'])
    ), "Object maps must contain a class_list (non-empty list of strings)"
