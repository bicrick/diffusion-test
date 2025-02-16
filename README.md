# Lightweight Diffusion Showcase

A minimal web application that demonstrates the diffusion model image generation process in real-time. This implementation uses a lightweight version of Stable Diffusion optimized for performance.

## Features

- Real-time visualization of the diffusion process
- Lightweight model implementation (Small Stable Diffusion V0)
- Simple and clean user interface
- Progress tracking for each generation step
- Minimal dependencies

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Enter your prompt in the text input field
2. Click "Generate" to start the diffusion process
3. Watch as the image gradually forms through each step
4. The final image will be displayed when generation is complete

## Technical Details

- Uses the Small Stable Diffusion V0 model (50% smaller than standard SD)
- Optimized for minimal memory usage with attention slicing
- 10 inference steps for faster generation
- Real-time visualization of each step
- Lightweight frontend with vanilla JavaScript

## Requirements

- Python 3.7+
- PyTorch
- Flask
- Modern web browser

## Notes

- First generation may take longer as the model needs to be loaded
- Generation speed depends on your hardware capabilities
- GPU is recommended but not required 