from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import io
import base64
import numpy as np
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the small model
model_id = "CompVis/stable-diffusion-v1-4"
pipe = None

def load_model():
    global pipe
    if pipe is None:
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,  # Use float32 for CPU
            use_safetensors=True
        )
        # Enable attention slicing for lower memory usage
        pipe.enable_attention_slicing()
        # Only enable model offload if CUDA is available
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
            pipe.enable_model_cpu_offload()

def get_image_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def get_latent_visualization(latents):
    # Normalize latents for visualization
    latents_vis = latents.detach().cpu().numpy()
    latents_vis = (latents_vis - latents_vis.min()) / (latents_vis.max() - latents_vis.min())
    latents_vis = (latents_vis * 255).astype(np.uint8)
    # Take first channel for visualization
    latent_image = Image.fromarray(latents_vis[0, 0])
    return get_image_base64(latent_image)

@socketio.on('start_generation')
def handle_generation(data):
    if pipe is None:
        load_model()
    
    prompt = data.get('prompt', '')
    num_steps = data.get('num_steps', 20)
    
    # Send initial state
    emit('generation_started', {
        'prompt': prompt,
        'total_steps': num_steps
    })
    
    def callback(step, timestep, latents):
        with torch.no_grad():
            # Decode the current latents to image
            image = pipe.decode_latents(latents.detach())
            image = pipe.numpy_to_pil(image)[0]
            
            # Get educational metadata
            progress = (step + 1) / num_steps
            noise_level = timestep.item()
            
            # Emit the current state
            emit('step_update', {
                'step': step,
                'progress': progress,
                'noise_level': noise_level,
                'decoded_image': get_image_base64(image),
                'latent_visualization': get_latent_visualization(latents),
                'explanation': f"Step {step + 1}/{num_steps}: Denoising at noise level {noise_level:.2f}"
            })
            
            # Add a small delay for educational purposes
            time.sleep(0.5)  # Adjust this value to control visualization speed
    
    try:
        image = pipe(
            prompt,
            num_inference_steps=num_steps,
            callback=callback,
            callback_steps=1
        ).images[0]
        
        # Send completion message
        emit('generation_completed', {
            'final_image': get_image_base64(image)
        })
    except Exception as e:
        emit('generation_error', {'error': str(e)})

@app.route('/')
def index():
    return send_file('static/index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080) 