import React, { useState } from 'react';
import { useStore } from '../store/useStore';
import { api } from '../utils/api';

export const EditingPanel: React.FC = () => {
  const { modelUrl, selectedType, setSelectedType, bodyMaterial, setBodyMaterial, fringeMaterial, setFringeMaterial } = useStore();
  const [fringeDensity, setFringeDensity] = useState(50);
  const [fringeLength, setFringeLength] = useState(50);
  const [paperThickness, setPaperThickness] = useState(50);
  const [bodyColor, setBodyColor] = useState('#FF6B6B');
  const [fringeColor, setFringeColor] = useState('#FFE66D');
  const [styleIntensity, setStyleIntensity] = useState(50);
  const [modelScale, setModelScale] = useState(100);
  const [geometrySmoothing, setGeometrySmoothing] = useState(50);
  const [makeManifold, setMakeManifold] = useState(false);
  const [editing, setEditing] = useState(false);
  const [history, setHistory] = useState<any[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);

  const handleEdit = async (param: string, value: any) => {
    if (!modelUrl) return;
    
    setEditing(true);
    
    // Save to history
    const currentState = {
      selectedType,
      bodyMaterial,
      fringeMaterial,
      fringeDensity,
      fringeLength,
      paperThickness,
      bodyColor,
      fringeColor,
      styleIntensity,
      modelScale,
      geometrySmoothing,
      makeManifold
    };
    
    const newHistory = [...history.slice(0, historyIndex + 1), currentState];
    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
    
    try {
      const editParams = {
        [param]: value,
        pinata_type: selectedType,
        body_material: bodyMaterial,
        fringe_material: fringeMaterial,
        fringe_density: fringeDensity / 100,
        fringe_length: fringeLength / 100,
        paper_thickness: paperThickness / 100,
        body_color: bodyColor,
        fringe_color: fringeColor,
        style_intensity: styleIntensity / 100,
        model_scale: modelScale / 100,
        geometry_smoothing: geometrySmoothing / 100,
        make_manifold: makeManifold
      };
      
      const result = await api.editModel(modelUrl, editParams);
      useStore.getState().setModelUrl(`/outputs/${result.model_path.split('/').pop()}`);
    } catch (error) {
      console.error('Error al editar:', error);
    } finally {
      setEditing(false);
    }
  };

  const handleUndo = () => {
    if (historyIndex > 0) {
      const prevState = history[historyIndex - 1];
      setSelectedType(prevState.selectedType);
      setBodyMaterial(prevState.bodyMaterial);
      setFringeMaterial(prevState.fringeMaterial);
      setFringeDensity(prevState.fringeDensity);
      setFringeLength(prevState.fringeLength);
      setPaperThickness(prevState.paperThickness);
      setBodyColor(prevState.bodyColor);
      setFringeColor(prevState.fringeColor);
      setStyleIntensity(prevState.styleIntensity);
      setModelScale(prevState.modelScale);
      setGeometrySmoothing(prevState.geometrySmoothing);
      setMakeManifold(prevState.makeManifold);
      setHistoryIndex(historyIndex - 1);
    }
  };

  const handleRedo = () => {
    if (historyIndex < history.length - 1) {
      const nextState = history[historyIndex + 1];
      setSelectedType(nextState.selectedType);
      setBodyMaterial(nextState.bodyMaterial);
      setFringeMaterial(nextState.fringeMaterial);
      setFringeDensity(nextState.fringeDensity);
      setFringeLength(nextState.fringeLength);
      setPaperThickness(nextState.paperThickness);
      setBodyColor(nextState.bodyColor);
      setFringeColor(nextState.fringeColor);
      setStyleIntensity(nextState.styleIntensity);
      setModelScale(nextState.modelScale);
      setGeometrySmoothing(nextState.geometrySmoothing);
      setMakeManifold(nextState.makeManifold);
      setHistoryIndex(historyIndex + 1);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-amber-800">Edición Avanzada</h2>
        <div className="flex gap-2">
          <button
            onClick={handleUndo}
            disabled={historyIndex <= 0}
            className="px-3 py-1 rounded-lg bg-gray-100 text-gray-700 disabled:opacity-50"
          >
            Deshacer
          </button>
          <button
            onClick={handleRedo}
            disabled={historyIndex >= history.length - 1}
            className="px-3 py-1 rounded-lg bg-gray-100 text-gray-700 disabled:opacity-50"
          >
            Rehacer
          </button>
        </div>
      </div>
      
      {!modelUrl ? (
        <p className="text-gray-500 text-center py-4">Genera un modelo primero para editar</p>
      ) : (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Densidad de Flecos: {fringeDensity}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={fringeDensity}
              onChange={(e) => setFringeDensity(Number(e.target.value))}
              onMouseUp={() => handleEdit('fringe_density', fringeDensity / 100)}
              className="w-full"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Longitud de Flecos: {fringeLength}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={fringeLength}
              onChange={(e) => setFringeLength(Number(e.target.value))}
              onMouseUp={() => handleEdit('fringe_length', fringeLength / 100)}
              className="w-full"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Grosor de Capa de Papel: {paperThickness}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={paperThickness}
              onChange={(e) => setPaperThickness(Number(e.target.value))}
              onMouseUp={() => handleEdit('paper_thickness', paperThickness / 100)}
              className="w-full"
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Color del Cuerpo
              </label>
              <input
                type="color"
                value={bodyColor}
                onChange={(e) => setBodyColor(e.target.value)}
                onBlur={() => handleEdit('body_color', bodyColor)}
                className="w-full h-10 rounded-lg"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Color de Flecos
              </label>
              <input
                type="color"
                value={fringeColor}
                onChange={(e) => setFringeColor(e.target.value)}
                onBlur={() => handleEdit('fringe_color', fringeColor)}
                className="w-full h-10 rounded-lg"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Intensidad de Estilo: {styleIntensity}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={styleIntensity}
              onChange={(e) => setStyleIntensity(Number(e.target.value))}
              onMouseUp={() => handleEdit('style_intensity', styleIntensity / 100)}
              className="w-full"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Escala del Modelo: {modelScale}%
            </label>
            <input
              type="range"
              min="50"
              max="200"
              value={modelScale}
              onChange={(e) => setModelScale(Number(e.target.value))}
              onMouseUp={() => handleEdit('model_scale', modelScale / 100)}
              className="w-full"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Suavizado de Geometría: {geometrySmoothing}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={geometrySmoothing}
              onChange={(e) => setGeometrySmoothing(Number(e.target.value))}
              onMouseUp={() => handleEdit('geometry_smoothing', geometrySmoothing / 100)}
              className="w-full"
            />
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="makeManifold"
              checked={makeManifold}
              onChange={(e) => {
                setMakeManifold(e.target.checked);
                handleEdit('make_manifold', e.target.checked);
              }}
              className="mr-2"
            />
            <label htmlFor="makeManifold" className="text-sm font-medium text-gray-700">
              Hacer Manifold (para impresión 3D)
            </label>
          </div>
          
          {editing && (
            <div className="flex items-center justify-center p-2">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-amber-500"></div>
              <p className="ml-2 text-gray-600">Aplicando cambios...</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
