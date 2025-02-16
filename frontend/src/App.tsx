import { useState, useEffect } from 'react'
import { io } from 'socket.io-client'
import { ArrowPathIcon } from '@heroicons/react/24/outline'

const socket = io('http://localhost:8080')

function App() {
  const [prompt, setPrompt] = useState('')
  const [currentImage, setCurrentImage] = useState<string | null>(null)
  const [progress, setProgress] = useState<number>(0)
  const [totalSteps, setTotalSteps] = useState<number>(0)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    socket.on('generation:progress', (data) => {
      setCurrentImage(data.image)
      setProgress(data.step)
      setTotalSteps(data.total_steps)
    })

    socket.on('generation:complete', (data) => {
      setCurrentImage(data.image)
      setIsGenerating(false)
      setProgress(0)
    })

    socket.on('generation:error', (data) => {
      setError(data.error)
      setIsGenerating(false)
    })

    return () => {
      socket.off('generation:progress')
      socket.off('generation:complete')
      socket.off('generation:error')
    }
  }, [])

  const handleGenerate = () => {
    if (!prompt.trim()) return
    
    setError(null)
    setIsGenerating(true)
    setProgress(0)
    
    socket.emit('generation:start', {
      prompt: prompt,
      num_inference_steps: 20
    })
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">
          Diffusion Visualization Tool
        </h1>
        
        <div className="mb-8">
          <div className="flex gap-4">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your prompt here..."
              className="flex-1 px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-blue-500"
              disabled={isGenerating}
            />
            <button
              onClick={handleGenerate}
              disabled={isGenerating || !prompt.trim()}
              className="px-6 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Generate
            </button>
          </div>
        </div>

        <div className="relative">
          {currentImage ? (
            <img
              src={currentImage}
              alt="Generated"
              className="w-full rounded-lg shadow-xl"
            />
          ) : (
            <div className="w-full h-96 bg-gray-800 rounded-lg flex items-center justify-center">
              <p className="text-gray-400">
                Generated image will appear here
              </p>
            </div>
          )}

          {isGenerating && (
            <div className="absolute inset-0 bg-black bg-opacity-50 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <ArrowPathIcon className="w-8 h-8 animate-spin mx-auto mb-2" />
                <p>
                  Generating... Step {progress} of {totalSteps}
                </p>
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-900 rounded-lg">
            <p className="text-red-200">{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
