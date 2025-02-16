from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import io
import base64
import numpy as np

app = Flask(__name__)
CORS(app)

# Initialize the small model
model_id = "madebyollin/sdxl-tiny"
pipe = None

def load_model():
    global pipe
    if pipe is None:
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            use_safetensors=True  # More memory efficient
        )
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        pipe.enable_attention_slicing()
        pipe.enable_model_cpu_offload()  # Further reduce memory usage

def get_image_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.route('/generate', methods=['POST'])
def generate():
    if pipe is None:
        load_model()
    
    data = request.json
    prompt = data.get('prompt', '')
    current_step = []
    
    def callback(step, timestep, latents):
        with torch.no_grad():
            image = pipe.decode_latents(latents.detach())
            image = pipe.numpy_to_pil(image)[0]
            current_step.append({
                'step': step,
                'image': get_image_base64(image)
            })
    
    # Generate image with minimal steps
    image = pipe(
        prompt,
        num_inference_steps=10,
        callback=callback,
        callback_steps=1
    ).images[0]
    
    return jsonify({
        'steps': current_step,
        'final_image': get_image_base64(image)
    })

@app.route('/')
def index():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 