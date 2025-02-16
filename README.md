# Diffusion Visualization Tool

An educational web application that visualizes the step-by-step process of AI image generation using diffusion models. Watch in real-time as your image emerges from random noise, providing insights into how diffusion-based image generation works.

## Features

- Real-time visualization of the diffusion process
- Step-by-step image generation display
- Lightweight, browser-friendly diffusion model
- Dockerized deployment for easy setup
- WebSocket-based real-time updates

## Tech Stack

- **Frontend**: React.js with Tailwind CSS
- **Backend**: Node.js with Express
- **Real-time Communication**: WebSocket
- **Containerization**: Docker
- **Image Generation**: Lightweight diffusion model

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- npm or yarn

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/diffusion-viz-tool.git
   cd diffusion-viz-tool
   ```

2. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the application at `http://localhost:3000`

## Development Setup

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Project Structure

```
.
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── services/
│   └── package.json
└── backend/
    ├── Dockerfile
    ├── src/
    │   ├── diffusion/
    │   ├── websocket/
    │   └── api/
    └── package.json
```

## Docker Configuration

The application consists of two main services:

1. **Frontend Container**: Serves the React application
   - Port: 3000
   - Environment: Production Node.js
   - Base image: node:18-alpine

2. **Backend Container**: Runs the Node.js server and diffusion model
   - Port: 8080
   - Environment: Production Node.js
   - Base image: node:18-alpine

## API Documentation

### WebSocket Events

- `generation:start`: Initiates image generation
- `generation:progress`: Receives intermediate generation steps
- `generation:complete`: Receives the final generated image
- `generation:error`: Receives error notifications

### HTTP Endpoints

- `POST /api/generate`: Start image generation
- `GET /api/status`: Check server status

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the open-source community for providing the lightweight diffusion model
- Inspired by educational tools in the AI/ML space