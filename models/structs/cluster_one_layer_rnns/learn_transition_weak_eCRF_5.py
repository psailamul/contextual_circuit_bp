

layer_structure = [
    {
        'layers': ['conv'],
        'weights': [64],
        'names': ['conv1_1'],
        'filter_size': [3],
        'normalization': ['contextual_frozen_connectivity_learned_transition_weak_eCRF'],
        'normalization_target': ['post'],
        'normalization_aux': {
            'timesteps': 5,
        },
    },
    {
        'layers': ['pool'],
        'weights': [None],
        'names': ['pool2'],
        'filter_size': [None]
    }
]
