import tensorflow as tf

# Check if TensorFlow can access GPU
if tf.test.is_gpu_available():
    print("GPU is available and TensorFlow is using it.")
else:
    print("GPU is not available or TensorFlow is not configured to use it.")
