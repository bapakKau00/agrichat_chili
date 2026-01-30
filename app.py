import os
import requests
from flask import Flask, render_template, request, jsonify, url_for
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Model
MODEL_PATH = 'best.pt'
try:
    model = YOLO(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

BOTPRESS_WEBHOOK_URL = "https://webhook.botpress.cloud/0b1eaf76-0a10-42f3-843f-37af309f495b" 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Grab IDs from the URL parameters
    conv_id = request.args.get('convId')
    user_id = request.args.get('userId')
    return render_template('index.html', convId=conv_id, userId=user_id)

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # 1. Grab the IDs that your website sent in the form
    conv_id = request.form.get('conversationId')
    user_id = request.form.get('userId')

    if not conv_id:
        print("WARNING: No conversationId received in the request!")

    if file and allowed_file(file.filename):
        # Process in memory without saving
        try:
            image = Image.open(file.stream)
        except Exception as e:
             return jsonify({'error': 'Invalid image file'}), 400

        if model:
            results = model(image)
            
            # Simple result processing: get the first result's top class name
            try:
                # Assuming single image inference
                result = results[0]
                
                diagnosis = "Uncertain"
                confidence = 0.0
                detections = []

                # Check if it's a classification model (has 'probs')
                if hasattr(result, 'probs') and result.probs is not None:
                    # Get the top 1 class and confidence
                    top1_index = result.probs.top1
                    diagnosis = result.names[top1_index]
                    confidence = float(result.probs.top1conf)
                    
                    # User requested highest detection only
                    detections.append({
                        "class": diagnosis,
                        "confidence": confidence
                    })
                
                # Check if it's an object detection model (has 'boxes') - Fallback
                elif hasattr(result, 'boxes') and result.boxes is not None:
                    all_detections = []
                    for box in result.boxes:
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = model.names[cls_id]
                        all_detections.append({
                            "class": class_name,
                            "confidence": conf
                        })
                    
                    if all_detections:
                        top_detection = max(all_detections, key=lambda x: x['confidence'])
                        diagnosis = top_detection['class']
                        confidence = top_detection['confidence']
                        # Return only the highest detection in the list as requested
                        detections.append(top_detection)
                    else:
                        diagnosis = "Healthy/None Detected"

                # Send to Botpress
                webhook_response = None
                try:
                    payload = {
                        "conversationId": conv_id, 
                        "userId": user_id,
                        "event": "disease_detection",
                        "diagnosis": diagnosis,
                        "confidence": round(confidence, 2)
                    }
                    # Uncomment to actually send when URL is ready
                    webhook_response = requests.post(BOTPRESS_WEBHOOK_URL, json=payload)
                    print(f"Would send to Botpress: {payload}")
                except Exception as w_err:
                    print(f"Webhook error: {w_err}")

                return jsonify({
                    'diagnosis': diagnosis,
                    'confidence': confidence,
                    'detections': detections # List with single top item
                })
            except Exception as e:
                return jsonify({'error': f'Inference error: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Model not loaded'}), 500

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
