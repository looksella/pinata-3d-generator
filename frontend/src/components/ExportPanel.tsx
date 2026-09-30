import React, { useState } from 'react';
import { useStore } from '../store/useStore';
import { api } from '../utils/api';

export const ExportPanel: React.FC = () => {
  const { modelUrl, selectedType, bodyMaterial, fringeMaterial, finishMaterial } = useStore();
  const [exporting, setExporting] = useState(false);
  const [exportFormat, setExportFormat] = useState('glb');
  const [blenderOpening, setBlenderOpening] = useState(false);

  const handleExport = async () => {
    if (!modelUrl) return;
    
    setExporting(true);
    
    try {
      const result = await api.exportModel(modelUrl, exportFormat);
      
      // Trigger download
      const link = document.createElement('a');
      link.href = result.output_path;
      link.download = `pinata.${exportFormat}`;
      link.click();
    } catch (error) {
      console.error('Error al exportar:', error);
    } finally {
      setExporting(false);
    }
  };

  const handleOpenInBlender = async () => {
    if (!modelUrl) return;
    
    setBlenderOpening(true);
    
    try {
      const materials = {
        body: bodyMaterial,
        fringe: fringeMaterial,
        finish: finishMaterial
      };
      
      await api.openInBlender(modelUrl, selectedType, materials);
    } catch (error) {
      console.error('Error al abrir Blender:', error);
    } finally {
      setBlenderOpening(false);
    }
  };

  const formats = [
    { id: 'glb', name: 'GLB (con texturas embebidas)', description: 'Formato principal, recomendado' },
    { id: 'gltf', name: 'glTF (separado)', description: 'Archivos separados' },
    { id: 'obj', name: 'OBJ + MTL + texturas', description: 'Compatible con la mayoría de software 3D' },
    { id: 'stl', name: 'STL (solo malla)', description: 'Para impresión 3D' },
    { id: '3mf', name: '3MF', description: 'Moderno, para impresión 3D' },
    { id: 'usdz', name: 'USDZ', description: 'Para AR en Apple' }
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-amber-800 mb-4">Exportar Modelo</h2>
      
      {!modelUrl ? (
        <p className="text-gray-500 text-center py-4">Genera un modelo primero para exportar</p>
      ) : (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Formato de Exportación
            </label>
            <div className="grid grid-cols-2 gap-3">
              {formats.map((format) => (
                <button
                  key={format.id}
                  onClick={() => setExportFormat(format.id)}
                  className={`p-3 rounded-lg border-2 transition-all text-left ${
                    exportFormat === format.id
                      ? 'border-amber-500 bg-amber-50'
                      : 'border-gray-200 hover:border-amber-300'
                  }`}
                >
                  <h4 className="font-medium text-gray-800">{format.name}</h4>
                  <p className="text-xs text-gray-500">{format.description}</p>
                </button>
              ))}
            </div>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={handleExport}
              disabled={exporting}
              className="flex-1 px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 disabled:bg-gray-300"
            >
              {exporting ? 'Exportando...' : 'Descargar Modelo'}
            </button>
            
            <button
              onClick={handleOpenInBlender}
              disabled={blenderOpening}
              className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300"
            >
              {blenderOpening ? 'Abriendo...' : 'Abrir en Blender'}
            </button>
          </div>
          
          {exporting && (
            <div className="flex items-center justify-center p-2">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-amber-500"></div>
              <p className="ml-2 text-gray-600">Preparando exportación...</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
