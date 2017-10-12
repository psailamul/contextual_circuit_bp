#Antolik data 

import numpy as np
from config import Config


class data_processing(object):
    """Template file for Antolik neural data."""
    def __init__(self):
        """Init global variables for contextual circuit bp."""
        self.name = 'Antolik_data'
        self.config = Config()
        self.output_size = [1, 1]
        self.im_size = (304, 608, 1)
        self.model_input_image_size = [152, 304, 1]
        self.meta = '/media/data_cifs/Antolik/tfrecords/ALLEN_all_neurons_meta.npy' #################
        self.default_loss_function = 'pearson'
        self.score_metric = 'pearson'
        self.preprocess = None

        # Load vars from the meta file
        meta_data = np.load(self.meta).item()
        self.folds = meta_data['folds']
        self.tf_reader = meta_data['tf_reader']
        self.tf_dict = {k: v for k, v in meta_data['tf_dict'].iteritems() if k in meta_data['tf_reader'].keys()}


# In [3]: test
Out[3]: array({'folds': {'train': 'train', 'val': 'val'}, \
    'im_size': (304, 608, 1), 
    'tf_dict': {'off_center_x': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'off_center_y': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'pupil_size': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'on_width_x': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'on_center_y': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'on_center_x': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'off_width_y': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'label': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'neural_trace_trimmed': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'running_speed': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'ROImask': FixedLenFeature(shape=[], dtype=tf.string, default_value=None), 'proc_stimuli': FixedLenFeature(shape=[], dtype=tf.string, default_value=None), 'eye_locations_spherical': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 'image': FixedLenFeature(shape=[], dtype=tf.string, default_value=None), 'cell_specimen_id': FixedLenFeature(shape=[], dtype=tf.int64, default_value=None)}, 'tf_reader': {'image': {'dtype': tf.float32, 'reshape': (304, 608, 1)}, 'cell_specimen_id': {'dtype': tf.float32, 'reshape': [1, 1]}, 'ROImask': {'dtype': tf.float32, 'reshape': (512, 512, 1)}, 'label': {'dtype': tf.float32, 'reshape': ()}}}, dtype=object)

