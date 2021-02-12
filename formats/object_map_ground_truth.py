def create_empty():
    return {
        'objects': [],
        'class_list': [],
        'synonyms': {}
    }


def create_empty_object():
    return {
        'class': "",
        'id': -1,
        'centroid': [0] * 3,
        'extent': [0] * 3,
        'is_group': False
    }
