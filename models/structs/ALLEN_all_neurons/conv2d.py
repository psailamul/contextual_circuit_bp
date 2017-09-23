"""2D convolutional model for Allen data."""

layer_structure = [
    {
        'layers': ['conv'],
        'weights': [64],
        'names': ['conv1_1'],
        'filter_size': [7],
        'activation': ['logistic'],
        'activation_target': ['post']
    },
    {
        'layers': ['pool'],
        'weights': [None],
        'names': ['pool1'],
        'filter_size': [None]
    },
    {
        'layers': ['fc'],
        'weights': [64],
        'names': ['fc2'],
        'flatten': [True],
        'flatten_target': ['pre'],
    }
]