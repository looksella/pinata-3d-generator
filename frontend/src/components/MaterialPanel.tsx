import React from 'react';
import { useStore } from '../store/useStore';

export const MaterialPanel: React.FC = () => {
  const { bodyMaterial, fringeMaterial, finishMaterial, setBodyMaterial, setFringeMaterial, setFinishMaterial } = useStore();

  const materials = {
    body: [
      { id: 'crepe', name: 'Papel Crepé', colors: ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF'] },
      { id: 'cartulina', name: 'Cartulina', colors: ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF'] },
      { id: 'papel-seda', name: 'Papel de Seda', colors: ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF'] },
      { id: 'papel-metalico', name: 'Papel Metálico', colors: ['#FFD700', '#C0C0C0', '#CD7F32', '#E5E4E2'] }
    ],
    fringe: [
      { id: 'corto', name: 'Fleco Corto', preview: 'short-fringe.png' },
      { id: 'medio', name: 'Fleco Medio', preview: 'medium-fringe.png' },
      { id: 'largo', name: 'Fleco Largo', preview: 'long-fringe.png' },
      { id: 'doble', name: 'Fleco Doble', preview: 'double-fringe.png' }
    ],
    finish: [
      { id: 'mate', name: 'Mate' },
      { id: 'brillante', name: 'Brillante' },
      { id: 'metalico', name: 'Metálico' }
    ]
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-amber-800 mb-4">Materiales</h2>
      
      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">Material del Cuerpo</h3>
          <div className="grid grid-cols-2 gap-3">
            {materials.body.map((mat) => (
              <button
                key={mat.id}
                onClick={() => setBodyMaterial(mat.id)}
                className={`p-3 rounded-lg border-2 transition-all ${
                  bodyMaterial === mat.id
                    ? 'border-amber-500 bg-amber-50'
                    : 'border-gray-200 hover:border-amber-300'
                }`}
              >
                <h4 className="font-medium text-gray-800">{mat.name}</h4>
                <div className="flex gap-1 mt-2">
                  {mat.colors.map((color, idx) => (
                    <div
                      key={idx}
                      className="w-6 h-6 rounded-full border border-gray-300"
                      style={{ backgroundColor: color }}
                    />
                  ))}
                </div>
              </button>
            ))}
          </div>
        </div>
        
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">Tipo de Fleco</h3>
          <div className="grid grid-cols-2 gap-3">
            {materials.fringe.map((fringe) => (
              <button
                key={fringe.id}
                onClick={() => setFringeMaterial(fringe.id)}
                className={`p-3 rounded-lg border-2 transition-all ${
                  fringeMaterial === fringe.id
                    ? 'border-amber-500 bg-amber-50'
                    : 'border-gray-200 hover:border-amber-300'
                }`}
              >
                <h4 className="font-medium text-gray-800">{fringe.name}</h4>
                <div className="mt-2 h-12 bg-gray-100 rounded flex items-center justify-center">
                  <img src={`/previews/${fringe.preview}`} alt={fringe.name} className="h-full object-contain" />
                </div>
              </button>
            ))}
          </div>
        </div>
        
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">Acabado</h3>
          <div className="grid grid-cols-3 gap-3">
            {materials.finish.map((finish) => (
              <button
                key={finish.id}
                onClick={() => setFinishMaterial(finish.id)}
                className={`p-3 rounded-lg border-2 transition-all ${
                  finishMaterial === finish.id
                    ? 'border-amber-500 bg-amber-50'
                    : 'border-gray-200 hover:border-amber-300'
                }`}
              >
                <h4 className="font-medium text-gray-800">{finish.name}</h4>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
