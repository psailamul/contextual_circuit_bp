import os
import numpy as np
import tensorflow as tf
from config import Config
from ops import tf_fun
from glob import glob
from tqdm import tqdm
import scipy
from scipy import io as spio
from scipy import misc


def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    def _check_keys(d):
        '''
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        '''
        for key in d:
            if isinstance(d[key], spio.matlab.mio5_params.mat_struct):
                d[key] = _todict(d[key])
        return d

    def _todict(matobj):
        '''
        A recursive function which constructs matobject nested dictionaries
        '''
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, spio.matlab.mio5_params.mat_struct):
                d[strg] = _todict(elem)
            elif isinstance(elem, np.ndarray):
                d[strg] = _tolist(elem)
            else:
                d[strg] = elem
        return d

    def _tolist(ndarray):
        '''
        A recursive function which constructs lists from cellarrays
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        '''
        elem_list = []
        for sub_elem in ndarray:
            if isinstance(sub_elem, spio.matlab.mio5_params.mat_struct):
                elem_list.append(_todict(sub_elem))
            elif isinstance(sub_elem, np.ndarray):
                elem_list.append(_tolist(sub_elem))
            else:
                elem_list.append(sub_elem)
        return elem_list
    data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)


class data_processing(object):
    def __init__(self):
        self.name = 'sheinberg_data_noise_subtracted'
        self.data_name = 'sheinberg_data'
        self.config = Config()
        self.output_size = [1, 1]
        self.im_size = [192, 256, 3]
        self.model_input_image_size = [192, 256, 3]
        self.num_rf_images = 2000
        self.default_loss_function = 'l2'
        self.score_metric = 'l2'
        self.preprocess = [None]
        self.im_ext = '.jpg'
        self.im_folder = 'scene_images'
        self.neural_data = 'spike'  # 'spike'
        self.val_set = -76
        self.save_npys = True
        self.num_channels = 33  # 32 with indexing from 1
        self.dates = ['100614', '100714', '100814', '100914']
        # Recording starts 200msec before onset.
        # Target is 50 - 150ms. = 270 - 370.
        self.spike_range = [250, 350]
        self.resize = [192, 256]
        self.folds = {
            'train': 'train',
            'test': 'test'}
        self.targets = {
            'image': tf_fun.bytes_feature,
            'label': tf_fun.float_feature
        }
        self.tf_dict = {
            'image': tf_fun.fixed_len_feature(dtype='string'),
            'label': tf_fun.fixed_len_feature(dtype='float')
        }
        self.tf_reader = {
            'image': {
                'dtype': tf.float32,
                'reshape': None
            },
            'label': {
                'dtype': tf.float32,
                'reshape': None
            }
        }

    def process_channels(self, data, it_images, bin_range):
        """Loop through channels and store data."""
        it_channel_key = np.asarray(data['channel'])
        it_neural = np.asarray(data['data'])
        unique_channels = np.unique(it_channel_key)
        channel_data = np.zeros((len(it_images), self.num_channels))
        for channel in unique_channels:
            #  Sum up spikes across spike-sorted channels
            channel_idx = np.where(it_channel_key == channel)[0]
            proc_it_neural = it_neural[channel_idx].sum(
                0)[bin_range].sum(0).astype(np.float32)
            channel_data[:, channel] = proc_it_neural
        return channel_data

    def get_data(self):

        # Find files
        neural_files = np.asarray(
            glob(
                os.path.join(
                    self.config.data_root,
                    self.data_name,
                    'scene*.mat')))
        scene_images = np.asarray(
            glob(
                os.path.join(
                    self.config.data_root,
                    self.data_name,
                    self.im_folder,
                    '*%s' % self.im_ext)))
        rf_files = np.asarray(
            glob(
                os.path.join(
                    self.config.data_root,
                    self.data_name,
                    'spot*.mat')))

        # Restrict to dates
        if self.dates is not None:
            neural_files = [
                f for f in neural_files
                if f.split('_')[-1].split('.')[0] in self.dates]
            neural_files.sort(
                key=lambda x: int(x.split('_')[-1].split('.')[0]))
            rf_files = [
                f for f in rf_files
                if f.split('_')[-1].split('.')[0] in self.dates]
            rf_files.sort(
                key=lambda x: int(x.split('_')[-1].split('.')[0]))

        # Process RF data
        bin_range = np.arange(self.spike_range[0], self.spike_range[1])
        rfs = []
        for f in tqdm(
                rf_files,
                total=len(rf_files),
                desc='Processing Sheinberg RFs'):
            data = loadmat(f)['data']
            rf_channel_data = self.process_channels(
                data[self.neural_data],
                np.zeros((self.num_rf_images)),
                bin_range)
            X = np.concatenate((
                np.asarray(data['trial_info']['stim_pos_y'])[:, None],
                np.asarray(data['trial_info']['stim_pos_x'])[:, None]),
                axis=1)
            preferred_rfs = [X[np.argmax(
                rf_channel_data[:, idx])] for idx in range(
                rf_channel_data.shape[-1])]
            rfs += [preferred_rfs]

        # Use the mean RF across sessions
        rfs = np.asarray(rfs)
        rfs = np.asarray([
            rfs[:, idx, :].mean(0)
            for idx in range(rfs.shape[1])])

        # Process scene data
        scene_labels = np.asarray(
            [x.split('/')[-1].split(self.im_ext)[0]
                for x in scene_images])
        files = []
        labels = []
        im_labels = []
        for f in tqdm(
                neural_files,
                total=len(neural_files),
                desc='Processing Sheinberg data'):
            data = loadmat(f)['data']
            stim_names = data['trial_info']['stim_names']
            it_images = []
            it_labels = []
            for st in stim_names:
                st = st.split('\x00')[0].replace(' ', '')
                it_images += [st]
                it_labels += [np.where(np.asarray(st) == scene_labels)]
            channel_data = self.process_channels(
                data[self.neural_data],
                it_images,
                bin_range)
            # print data['trial_info']['date']
            # TODO: Visualize gaussian-smoothed spikes here
            files += [it_images]
            im_labels += [it_labels]
            labels += [channel_data]

        # Load and process all images
        cat_files = np.concatenate(files)
        unique_images = np.unique(cat_files)
        all_images = {}
        for im in unique_images:
            it_image = misc.imread(
                os.path.join(
                    self.config.data_root,
                    self.data_name,
                    self.im_folder,
                    '%s%s' % (im, self.im_ext)))
            if self.resize is not None:
                it_image = misc.imresize(it_image, self.resize)
            all_images[im] = np.expand_dims(it_image, axis=0)

        # Slice an image array
        sliced_images = []
        for im in cat_files:
            sliced_images += [all_images[im]]
        sliced_images = np.asarray(sliced_images).squeeze()

        # Prepare data and build up extra regressors for linear model
        data_matrix = np.concatenate(labels, axis=0)
        out_data_matrix = data_matrix.tolist()
        run_idx = np.concatenate([
            np.zeros((len(f))) for f in files])

        # Create across-session stimulus normalized data
        im_means = {}
        for im in unique_images:
            mask = np.asarray(im) == cat_files
            im_means[im] = data_matrix[mask, :].mean(0)

        across_session_data_matrix = []
        for idx, im in enumerate(cat_files):
            across_session_data_matrix += [data_matrix[idx] - im_means[im]]
        across_session_data_matrix = np.asarray(across_session_data_matrix)

        # Split labels/files into training/testing (leave one session out).
        out_files = {  # Images
            'train': sliced_images[:self.val_set],
            'val': sliced_images[self.val_set:]
        }
        out_labels = {  # Neural data
            'train': out_data_matrix[:self.val_set],
            'val': out_data_matrix[self.val_set:]
        }

        if self.save_npys:
            out_file = os.path.join(
                self.config.data_root,
                self.name,
                self.name)
            np.savez(
                out_file,
                data_matrix=data_matrix,
                across_session_data_matrix=across_session_data_matrix,
                im_means=im_means,
                all_images=sliced_images,
                rfs=rfs,
                run_idx=run_idx)
        return out_files, out_labels
