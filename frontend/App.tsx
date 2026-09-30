import React, { useState, useEffect } from 'react';
import { ImageUploader } from './components/ImageUploader';
import { StyleSelector } from './components/StyleSelector';
import { PinataTypeSelector } from './components/PinataTypeSelector';
import { MaterialPanel } from './components/MaterialPanel';
import { ModelViewer } from './components/ModelViewer';
import { EditingPanel } from './components/EditingPanel';
import { ExportPanel } from './components/ExportPanel';
import { HistoryPanel } from './components/HistoryPanel';
import { useStore } from './store/useStore';
import { api } from './utils/api';

const App: React.FC = () => {
  const { currentStep, setCurrentStep, gpuInfo, setGpuInfo } = useStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Obtener información de GPU al cargar
    api.getGpuInfo()
      .then(info => {
        setGpuInfo(info);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error al obtener información de GPU:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-amber-50 to-rose-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500 mx-auto"></div>
          <p className="mt-4 text-amber-800">Cargando sistema...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-rose-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-amber-800">Generador de Piñatas 3D</h1>
            {gpuInfo && (
              <div className="text-sm text-gray-600">
                {gpuInfo.available ? (
                  <span className="flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                    GPU: {gpuInfo.name} ({gpuInfo.total_memory_mb} MB)
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <span className="w-2 h-2 bg-orange-500 rounded-full"></span>
                    Modo híbrido (sin GPU NVIDIA)
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-6">
            <ImageUploader />
            <StyleSelector />
            <PinataTypeSelector />
            <MaterialPanel />
          </div>
          
          <div className="lg:col-span-2 space-y-6">
            <ModelViewer />
            <EditingPanel />
            <ExportPanel />
            <HistoryPanel />
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
