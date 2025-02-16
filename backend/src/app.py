from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the small stable diffusion pipeline
device = "cpu"
model_id = "OFA-Sys/small-stable-diffusion-v0"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float32,
    safety_checker=None  # Disable safety checker for speed
)
pipe = pipe.to(device)

# Use DPMSolver scheduler for faster inference
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# Enable optimizations
pipe.enable_attention_slicing()
torch.set_grad_enabled(False)  # Disable gradient computation
torch.set_num_threads(4)  # Limit CPU threads

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

@app.route('/api/status')
def status():
    return jsonify({
        "status": "healthy",
        "model": model_id,
        "device": device,
        "torch_threads": torch.get_num_threads(),
        "scheduler": pipe.scheduler.__class__.__name__
    })

@socketio.on('generation:start')
def handle_generation_start(data):
    try:
        prompt = data.get('prompt', '')
        num_inference_steps = data.get('num_inference_steps', 10)  # Using 10 steps as recommended
        
        def callback_fn(step: int, timestep: int, latents: torch.FloatTensor):
            # Convert latents to image
            with torch.no_grad():
                image = pipe.decode_latents(latents)
                image = pipe.numpy_to_pil(image)[0]
                
                # Emit progress
                emit('generation:progress', {
                    'step': step,
                    'total_steps': num_inference_steps,
                    'image': image_to_base64(image)
                })
        
        # Generate the image
        with torch.no_grad():
            image = pipe(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                callback=callback_fn,
                callback_steps=1,
                guidance_scale=7.5,
                height=512,
                width=512
            ).images[0]
        
        # Emit the final result
        emit('generation:complete', {
            'image': image_to_base64(image)
        })
        
    except Exception as e:
        emit('generation:error', {'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True) 