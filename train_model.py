import tensorflow as tf
from tensorflow.keras import layers
import os

# 1. Configurar ruta local
data_dir = 'datos_plantas' 
t_img = 150
batch_s = 32

# 2. Cargar imágenes desde tu carpeta (esto reemplaza a tfds.load)
datos_train = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(t_img, t_img),
  batch_size=batch_s
)

datos_test = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(t_img, t_img),
  batch_size=batch_s
)

# 3. Normalizar (como en tu taller original)
def normalize(image, label):
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

datos_train = datos_train.map(normalize)
datos_test = datos_test.map(normalize)

# Al final de tu script
model.save('models/modelo_plantas_tf.h5')
print("✅ ¡Modelo listo para AIPLANTS!")