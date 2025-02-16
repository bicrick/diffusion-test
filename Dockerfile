FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install CPU-optimized PyTorch first
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Then install other requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables for better performance
ENV PYTORCH_ENABLE_MPS_FALLBACK=1
ENV TRANSFORMERS_OFFLINE=1

# Download and cache the model during build
RUN python3 -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('CompVis/stable-diffusion-v1-4', use_safetensors=True, torch_dtype='float32')"

# Expose the port
EXPOSE 8080

# Run the application
CMD ["python3", "app.py"] 