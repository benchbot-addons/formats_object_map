def create_empty():
    return {
        'objects': [],
        'synonyms': {}
    }


def create_empty_object():
    return {
        'class': "",
        'id': "",
        'centroid': [0] * 3,
        'extent': [0] * 3,
        'is_group': False
    }
