"""Class to specify all DNN experiments."""
import os
import numpy as np


class experiments():
    """Class for experiments."""

    def __getitem__(self, name):
        """Method for addressing class methods."""
        return getattr(self, name)

    def __contains__(self, name):
        """Method for checking class contents."""
        return hasattr(self, name)

    def globals(self):
        """Global variables for all experiments."""
        return {
            'batch_size': 64,  # Train/val batch size.
            'data_augmentations': [
                [
                    'random_crop',
                    'left_right'
                ]
            ],  # TODO: document all data augmentations.
            'epochs': 200,
            'shuffle': True,  # Shuffle data.
            'validation_iters': 5000,  # How often to evaluate validation.
            'num_validation_evals': 100,  # How many validation batches.
            'top_n_validation': 0,  # Set to 0 to save all checkpoints.
            'early_stop': False,  # Stop training if the loss stops improving.
            'save_weights': False,  # Save model weights on validation evals.
            'optimizer_constraints': None  # A {var name: bound} dictionary.
        }

    def add_globals(self, exp):
        """Add attributes to this class."""
        for k, v in self.globals().iteritems():
            exp[k] = v
        return exp

    def perceptual_iq_hp_optimization(self):
        """Each key in experiment_dict must be manually added to the schema.

        If using grid-search -- put hps in lists.
        If using hp-optim, do not use lists except for domains.
        """
        model_folder = 'perceptual_iq_hp_optimization'
        exp = {
            'experiment_name': model_folder,
            'hp_optim': 'gpyopt',
            'hp_multiple': 10,
            'lr': 1e-4,
            'lr_domain': [1e-1, 1e-5],
            'loss_function': None,  # Leave as None to use dataset default
            'optimizer': 'adam',
            'regularization_type': None,  # [None, 'l1', 'l2'],
            'regularization_strength': 1e-5,
            'regularization_strength_domain': [1e-1, 1e-7],
            # 'timesteps': True,
            'model_struct': [
                os.path.join(model_folder, 'divisive_1l'),
                os.path.join(model_folder, 'layer_1l'),
                os.path.join(model_folder, 'divisive_2l'),
                os.path.join(model_folder, 'layer_2l'),
            ],
            'dataset': 'ChallengeDB_release'
        }
        return self.add_globals(exp)  # Add globals to the experiment

    def two_layer_conv_mlp(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'two_layer_conv_mlp'
        exp = {
            'experiment_name': [model_folder],
            'lr': [1e-5],
            'loss_function': ['cce'],
            'optimizer': ['adam'],
            'regularization_type': [None],  # [None, 'l1', 'l2'],
            'regularization_strength': [0.005],
            'model_struct': [
                os.path.join(model_folder, 'divisive'),
                os.path.join(model_folder, 'batch'),
                os.path.join(model_folder, 'layer'),
                os.path.join(model_folder, 'lrn'),
                os.path.join(model_folder, 'contextual'),
                os.path.join(model_folder, 'contextual_rnn'),
                os.path.join(model_folder, 'contextual_rnn_no_relu'),
                # os.path.join(model_folder, 'contextual_selu'),
                # os.path.join(model_folder, 'contextual_rnn_selu'),
            ],
            'dataset': ['cifar_10']
        }
        return self.add_globals(exp)  # Add globals to the experiment

    def test_conv(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'test_conv'
        exp = {
            'experiment_name': [model_folder],
            'lr': list(np.logspace(-5, -1, 5, base=10)),
            'loss_function': ['cce'],
            'optimizer': ['adam'],
            'regularization_type': [None],
            'regularization_strength': [None],
            'model_struct': [
                os.path.join(model_folder, 'test'),
            ],
            'dataset': ['mnist', 'cifar_10']
        }
        return self.add_globals(exp)  # Add globals to the experiment

    def test_fc(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'test_fc'
        exp = {
            'experiment_name': [model_folder],
            'lr': list(np.logspace(-5, -1, 5, base=10)),
            'loss_function': ['cce'],
            'optimizer': ['sgd'],
            'regularization_type': [None],
            'regularization_strength': [None],
            'model_struct': [
                os.path.join(model_folder, 'test'),
            ],
            'dataset': ['mnist', 'cifar_10']
        }
        return self.add_globals(exp)  # Add globals to the experiment

    def test_res(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'test_res'
        exp = {
            'experiment_name': [model_folder],
            'lr': list(np.logspace(-5, -1, 5, base=10)),
            'loss_function': ['cce'],
            'optimizer': ['adam'],
            'regularization_type': [None],
            'regularization_strength': [None],
            'model_struct': [
                os.path.join(model_folder, 'test'),
            ],
            'dataset': ['mnist', 'cifar_10']
        }
        return self.add_globals(exp)  # Add globals to the experiment

    def coco_cnn(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'coco_cnn'
        exp = {
            'experiment_name': [model_folder],
            'lr': [3e-4],
            'loss_function': ['sigmoid'],
            'optimizer': ['adam'],
            'model_struct': [
                os.path.join(model_folder, 'cnn'),
                os.path.join(model_folder, 'contextual_cnn')
            ],
            'dataset': ['coco_2014']
        }
        exp = self.add_globals(exp)  # Add globals to the experiment'
        exp['epochs'] = 200
        exp['batch_size'] = 16  # Train/val batch size.
        exp['save_weights'] = True
        return exp

    def challengedb_cnns(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'challengedb_cnns'
        exp = {
            'experiment_name': [model_folder],
            'lr': [1e-3],
            'loss_function': ['l2'],
            'optimizer': ['adam'],
            'model_struct': [
                os.path.join(model_folder, 'cnn'),
                os.path.join(model_folder, 'contextual_cnn')
            ],
            'dataset': ['ChallengeDB_release']
        }
        exp = self.add_globals(exp)  # Add globals to the experiment'
        exp['epochs'] = 200
        exp['batch_size'] = 8  # Train/val batch size.
        exp['save_weights'] = True
        return exp

    def contextual_model_paper(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'contextual_model_paper'
        exp = {
            'experiment_name': [model_folder],
            'lr': [5e-3],
            'loss_function': ['l2'],
            'optimizer': ['adam'],
            'q_t': [1e-3, 1e-1],
            'p_t': [1e-2, 1e-1, 1],
            't_t': [1e-2, 1e-1, 1],
            'timesteps': [5, 10],
            'model_struct': [
                # os.path.join(model_folder, 'divisive_paper_rfs'),
                os.path.join(model_folder, 'contextual_paper_rfs'),
                # os.path.join(model_folder, 'divisive'),
                # os.path.join(model_folder, 'contextual'),
            ],
            'dataset': ['contextual_model_multi_stimuli']
        }
        exp = self.add_globals(exp)  # Add globals to the experiment'
        exp['data_augmentations'] = [[None]]
        exp['epochs'] = 1000
        exp['save_weights'] = True
        return exp

    def ALLEN_selected_cells_103(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'ALLEN_selected_cells_103'
        exp = {
            'experiment_name': [model_folder],
            'lr': [1e-3],
            'loss_function': ['l2'],
            'optimizer': ['adam'],
            'regularization_type': ['l2'],  # [None, 'l1', 'l2'],
            'regularization_strength': [1e-7],
            'model_struct': [
                os.path.join(model_folder, 'conv2d'),
                os.path.join(model_folder, 'adj_norm_conv2d'),
                os.path.join(model_folder, 'scalar_norm_conv2d'),
                os.path.join(model_folder, 'vector_norm_conv2d'),
                os.path.join(model_folder, 'DoG'),
            ],
            'dataset': ['ALLEN_selected_cells_103']
        }
        exp = self.add_globals(exp)  # Add globals to the experiment'
        exp['data_augmentations'] = [['resize']]
        exp['epochs'] = 100
        exp['validation_iters'] = 500
        exp['num_validation_evals'] = 100
        exp['batch_size'] = 16  # Train/val batch size.
        return exp

    def ALLEN_random_cells_103(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'ALLEN_random_cells_103'
        exp = {
            'experiment_name': [model_folder],
            'lr': [1e-3],
            'loss_function': ['l2'],
            'optimizer': ['hessian'],
            'regularization_type': ['l2'],  # [None, 'l1', 'l2'],
            'regularization_strength': [1e-7],
            'model_struct': [
                os.path.join(model_folder, 'DoG'),
            ],
            'dataset': ['ALLEN_random_cells_103']
        }
        exp = self.add_globals(exp)  # Add globals to the experiment'
        exp['data_augmentations'] = [['resize']]
        exp['epochs'] = 100
        exp['validation_iters'] = 500
        exp['num_validation_evals'] = 100
        exp['batch_size'] = 16  # Train/val batch size.
        exp['optimizer_constraints'] = {'dog1': (0, 10)}
        return exp

    def ALLEN_selected_cells_1(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'ALLEN_selected_cells_1'
        exp = {
            'experiment_name': [model_folder],
            'lr': [1e-3],
            'loss_function': ['l2'],
            'optimizer': ['adam'],
            'regularization_type': ['l2'],  # [None, 'l1', 'l2'],
            'regularization_strength': [1e-7],
            'model_struct': [
                os.path.join(model_folder, 'conv2d'),
                os.path.join(model_folder, 'sep_conv2d'),
                os.path.join(model_folder, 'DoG'),
            ],
            'dataset': ['ALLEN_selected_cells_1']
        }
        exp = self.add_globals(exp)  # Add globals to the experiment'
        exp['data_augmentations'] = [['resize']]
        exp['epochs'] = 100
        exp['validation_iters'] = 500
        exp['num_validation_evals'] = 100
        exp['batch_size'] = 32  # Train/val batch size.
        return exp

    def ALLEN_ss_cells_1_movies(self):
        """Each key in experiment_dict must be manually added to the schema."""
        model_folder = 'ALLEN_ss_cells_1_movies'
        exp = {
            'experiment_name': [model_folder],
            'lr': [1e-3],
            'loss_function': ['l2'],
            'optimizer': ['adam'],
            'regularization_type': ['l2'],  # [None, 'l1', 'l2'],
            'regularization_strength': [1e-7],
            'model_struct': [
                os.path.join(model_folder, 'conv2d'),
                os.path.join(model_folder, 'sep_conv2d'),
                os.path.join(model_folder, 'DoG'),
            ],
            'dataset': ['ALLEN_ss_cells_1_movies']
        }
        exp = self.add_globals(exp)  # Add globals to the experiment'
        exp['data_augmentations'] = [['resize']]
        exp['epochs'] = 100
        exp['validation_iters'] = 500
        exp['num_validation_evals'] = 100
        exp['batch_size'] = 32  # Train/val batch size.
        return exp
