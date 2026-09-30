import React, { useRef, useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, Grid, GizmoHelper, GizmoViewport, useGLTF } from '@react-three/drei';
import { useStore } from '../store/useStore';
import * as THREE from 'three';

const Model: React.FC<{ url: string; viewMode: string }> = ({ url, viewMode }) => {
  const { scene } = useGLTF(url);
  
  React.useEffect(() => {
    scene.traverse((child: THREE.Object3D) => {
      if (child instanceof THREE.Mesh) {
        if (viewMode === 'wireframe') {
          child.material = new THREE.MeshBasicMaterial({ wireframe: true, color: '#FF6B6B' });
        } else if (viewMode === 'solid') {
          child.material = new THREE.MeshStandardMaterial({ color: '#FF6B6B', roughness: 0.7, metalness: 0.1 });
        }
        // For 'textured', keep original materials
      }
    });
  }, [scene, viewMode]);
  
  return <primitive object={scene} />;
};

export const ModelViewer: React.FC = () => {
  const { modelUrl, viewMode, setViewMode } = useStore();
  const [autoRotate, setAutoRotate] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');

  const handleGenerate = async () => {
    setGenerating(true);
    setProgress(0);
    setMessage('Iniciando generación...');
    
    // WebSocket connection for generation
    const ws = new WebSocket('ws://localhost:8000/ws/generate');
    
    ws.onopen = () => {
      const params = {
        image_path: useStore.getState().uploadedImage,
        pinata_type: useStore.getState().selectedType,
        style_mode: useStore.getState().selectedStyle,
        materials: {
          body: useStore.getState().bodyMaterial,
          fringe: useStore.getState().fringeMaterial,
          finish: useStore.getState().finishMaterial
        }
      };
      ws.send(JSON.stringify(params));
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.progress !== undefined) {
        setProgress(data.progress);
        setMessage(data.message);
      }
      if (data.model_path) {
        useStore.getState().setModelUrl(`/outputs/${data.model_path.split('/').pop()}`);
        setGenerating(false);
      }
      if (data.error) {
        setMessage(`Error: ${data.error}`);
        setGenerating(false);
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setMessage('Error de conexión');
      setGenerating(false);
    };
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-amber-800">Visor 3D</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('solid')}
            className={`px-3 py-1 rounded-lg ${
              viewMode === 'solid' ? 'bg-amber-500 text-white' : 'bg-gray-100 text-gray-700'
            }`}
          >
            Sólido
          </button>
          <button
            onClick={() => setViewMode('wireframe')}
            className={`px-3 py-1 rounded-lg ${
              viewMode === 'wireframe' ? 'bg-amber-500 text-white' : 'bg-gray-100 text-gray-700'
            }`}
          >
            Estructura
          </button>
          <button
            onClick={() => setViewMode('textured')}
            className={`px-3 py-1 rounded-lg ${
              viewMode === 'textured' ? 'bg-amber-500 text-white' : 'bg-gray-100 text-gray-700'
            }`}
          >
            Texturizado
          </button>
          <button
            onClick={() => setAutoRotate(!autoRotate)}
            className={`px-3 py-1 rounded-lg ${
              autoRotate ? 'bg-amber-500 text-white' : 'bg-gray-100 text-gray-700'
            }`}
          >
            360°
          </button>
        </div>
      </div>
      
      <div className="h-96 bg-gray-50 rounded-lg overflow-hidden relative">
        {modelUrl ? (
          <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
            <ambientLight intensity={0.5} />
            <directionalLight position={[10, 10, 5]} intensity={1} />
            <Environment preset="studio" />
            
            <Suspense fallback={null}>
              <Model url={modelUrl} viewMode={viewMode} />
            </Suspense>
            
            <Grid
              args={[10, 10]}
              cellSize={0.5}
              cellThickness={0.5}
              cellColor="#gray"
              sectionSize={2}
              sectionThickness={1}
              sectionColor="#amber"
              fadeDistance={30}
              fadeStrength={1}
              followCamera={false}
              infiniteGrid
            />
            
            <OrbitControls autoRotate={autoRotate} />
            <GizmoHelper alignment="bottom-right" margin={[80, 80]}>
              <GizmoViewport axisColors={['#FF6B6B', '#4ECDC4', '#FFE66D']} labelColor="black" />
            </GizmoHelper>
          </Canvas>
        ) : (
          <div className="flex items-center justify-center h-full">
            {generating ? (
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500 mx-auto"></div>
                <p className="mt-4 text-gray-600">{message}</p>
                <div className="mt-2 w-64 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-amber-500 h-2 rounded-full transition-all"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
                <p className="mt-1 text-sm text-gray-500">{progress}%</p>
              </div>
            ) : (
              <div className="text-center">
                <p className="text-gray-500">No hay modelo generado</p>
                <button
                  onClick={handleGenerate}
                  disabled={!useStore.getState().uploadedImage}
                  className="mt-4 px-6 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  Generar modelo 3D
                </button>
                {!useStore.getState().uploadedImage && (
                  <p className="mt-2 text-sm text-gray-400">Sube una imagen primero</p>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
