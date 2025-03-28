import cv2
import numpy as np

# Function to preprocess image
def prepare_image(img_path):
    img = cv2.imread(img_path) # read image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # bgr to rgb
    resized_img = cv2.resize(img, (224, 224)) # resize image to 224*224
    img_array = np.array(resized_img, dtype=np.float32) / 255.0 # normalize
    img_array = np.expand_dims(img_array, axis=0) # expand diameter to 0 (means single)
    return img_array