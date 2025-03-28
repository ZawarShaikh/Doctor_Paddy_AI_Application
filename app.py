from flask import Flask, render_template, request, redirect, flash
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow import image 
import numpy as np
import cv2
from preprocess_image import prepare_image


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.secret_key = os.urandom(24)
print("Secret key : ", app.secret_key)


# Email settings
SMTP_SERVER = "smtp.gmail.com"  # Change if using another email provider
SMTP_PORT = 465
EMAIL_ADDRESS = "mohammadzawar892@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "zaan123@AZ123"  # Replace with your app password


# Load trained ResNet-50 model
model = tf.keras.models.load_model('models/vgg19_rice_disease_model_fintuned.h5')

# Class names and number
class_names = [
    'Bacterial Leaf Blight', 'Bacterial Leaf Streak', 'Bacterial Panicle Blight', 'Blast', 
    'Brown Spot', 'Dead Heart', 'Downy Mildew', 'Hispa', 'Normal', 'Tungro'
           ]
classes_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

classes = [
    'bacterial_leaf_blight', 'bacterial_leaf_streak', 'bacterial_panicle_blight', 'blast', 
    'brown_spot', 'dead_heart', 'downy_hildew', 'hispa', 'normal', 'tungro'
    ]

# recommendations
recommendations = {
    'bacterial_leaf_blight': [
        "Use resistant varieties (e.g., IR64, Samba Mahsuri Sub1).",
        "Reduce nitrogen fertilizer usage.",
        "Practice crop rotation to avoid continuous rice cropping.",
        "Maintain proper drainage and avoid water stagnation.",
        "Apply copper oxychloride (3g/L) or streptomycin sulfate (0.1g/L)."
    ],
    'bacterial_leaf_streak': [
        "Use resistant/tolerant varieties.",
        "Minimize mechanical injuries to plants.",
        "Apply balanced fertilizers and reduce nitrogen usage.",
        "Use copper oxychloride (2.5g/L) or kasugamycin (0.2g/L).",
        "Improve field sanitation by removing infected plant debris."
    ],
    'bacterial_panicle_blight': [
        "Use disease-free seeds.",
        "Avoid excessive nitrogen fertilizer.",
        "Ensure proper plant spacing to improve air circulation.",
        "Remove and destroy infected plant debris.",
        "Apply bactericide sprays if necessary (streptomycin sulfate 0.1g/L)."
    ],
    'blast': [
        "Use resistant varieties such as IR64 and NSIC Rc222.",
        "Apply recommended doses of nitrogen fertilizer.",
        "Ensure proper field drainage and avoid water stagnation.",
        "Use fungicides like tricyclazole (0.6g/L) or isoprothiolane (1.5ml/L).",
        "Avoid late planting and dense sowing."
    ],
    'brown_spot': [
        "Use balanced fertilizers, especially potassium and phosphorus.",
        "Ensure proper drainage and avoid waterlogging.",
        "Apply organic matter or farmyard manure to improve soil health.",
        "Use fungicides like mancozeb (2.5g/L) or propiconazole (1ml/L).",
        "Remove infected plant residues after harvest."
    ],
    'dead_heart': [
        "Destroy infected plants early to prevent spread.",
        "Use light traps to monitor insect population.",
        "Encourage natural predators like spiders and parasitoid wasps.",
        "Apply insecticides like chlorantraniliprole (0.3ml/L) if infestation is severe.",
        "Maintain proper field sanitation."
    ],
    'downy_mildew': [
        "Use disease-resistant varieties.",
        "Avoid overwatering and ensure proper field drainage.",
        "Rotate crops to reduce pathogen buildup in the soil.",
        "Apply fungicides like metalaxyl (1.5g/L) or mancozeb (2g/L).",
        "Destroy infected plant parts to prevent further spread."
    ],
    'hispa': [
        "Handpick and destroy infected leaves to reduce pest population.",
        "Encourage natural enemies like parasitic wasps and lady beetles.",
        "Avoid excessive nitrogen fertilizer as it attracts pests.",
        "Use neem-based biopesticides or insecticides like lambda-cyhalothrin (0.5ml/L).",
        "Flood the field for a short period to kill larvae."
    ],
    'tungro': [
        "Use tungro-resistant rice varieties.",
        "Control vector insects (green leafhoppers) using insecticides like imidacloprid (0.3ml/L).",
        "Plant at recommended spacing to reduce vector movement.",
        "Rogue infected plants to prevent disease spread.",
        "Avoid overlapping planting seasons to minimize vector population."
    ]
}



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Predict disease
            img_array = prepare_image(filepath)
            predictions = model.predict(img_array)
            predicted_class = classes_num[np.argmax(predictions)]
            confidence = np.max(predictions) * 100
            
            # selecting the class name based on prediction class (eg, 0,1,2,3)
            prediction_class = classes[predicted_class]
            prediction_class_name = class_names[predicted_class]
            
            recommended_actions = recommendations.get(prediction_class, 
                                                      ["No specific recommendations available."]
                                                      )
            
            return render_template('detect.html', 
                                   prediction=prediction_class_name, 
                                   confidence=confidence, 
                                   file_name=file.filename, 
                                   recommendations=recommended_actions
                                   )

    return render_template('detect.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        #print(f"New Message: {name}, {email}, {message}")  # Placeholder for processing
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
