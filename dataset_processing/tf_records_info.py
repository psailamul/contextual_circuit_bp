# tfrecords 

'folds': {'train': 'train', 'val': 'val'}, 
'im_size': (304, 608, 1), 

'tf_dict': 
{
'off_center_x': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'off_center_y': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'pupil_size': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'on_width_x': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'on_center_y': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'on_center_x': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'off_width_y': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'label': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'neural_trace_trimmed': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'running_speed': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'ROImask': FixedLenFeature(shape=[], dtype=tf.string, default_value=None), 
'proc_stimuli': FixedLenFeature(shape=[], dtype=tf.string, default_value=None), 
'eye_locations_spherical': FixedLenFeature(shape=[], dtype=tf.float32, default_value=None), 
'image': FixedLenFeature(shape=[], dtype=tf.string, default_value=None), 
'cell_specimen_id': FixedLenFeature(shape=[], dtype=tf.int64, default_value=None)}, 

'tf_reader': 
{	'image':  {'dtype': tf.float32,  'reshape': (304, 608, 1)}, 
	'cell_specimen_id': {'dtype': tf.float32, 'reshape': [1, 1]},
	'ROImask': {'dtype': tf.float32, 'reshape': (512, 512, 1)}, 
	'label': {'dtype': tf.float32, 'reshape': ()


