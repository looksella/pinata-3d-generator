import React from 'react';
import { useStore } from '../store/useStore';

export const PinataTypeSelector: React.FC = () => {
  const { selectedType, setSelectedType } = useStore();

  const pinataTypes = [
    {
      id: 'tambor',
      name: 'Piñata de Tambor (o Silueta)',
      description: 'Estilo plano o semi-plano con forma de silueta',
      icon: '🥁'
    },
    {
      id: 'tambor-alto-relieve',
      name: 'Piñata de Tambor con Alto Relieve',
      description: 'Base de tambor con apliques 3D y detalles en relieve',
      icon: '🎭'
    },
    {
      id: 'escultura-3d',
      name: 'Piñata Escultura o 3D Completa',
      description: 'Piñata volumétrica completamente tridimensional',
      icon: '🎨'
    },
    {
      id: 'rostro',
      name: 'Piñata de Rostro (o Tipo Espejo)',
      description: 'Estilo frontal con espalda plana',
      icon: '😊'
    },
    {
      id: 'tira-listones',
      name: 'Piñata de Tira o de Listones',
      description: 'Diseñada con listones para apertura',
      icon: '🎀'
    },
    {
      id: 'globo-estallido',
      name: 'Piñata de Globo (o Estallido)',
      description: 'Estilo globo o de estallido',
      icon: '🎈'
    }
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-amber-800 mb-4">Tipo de Piñata</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {pinataTypes.map((type) => (
          <button
            key={type.id}
            onClick={() => setSelectedType(type.id)}
            className={`p-4 rounded-lg border-2 transition-all ${
              selectedType === type.id
                ? 'border-amber-500 bg-amber-50'
                : 'border-gray-200 hover:border-amber-300'
            }`}
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">{type.icon}</span>
              <div className="text-left">
                <h3 className="font-medium text-gray-800">{type.name}</h3>
                <p className="text-sm text-gray-500">{type.description}</p>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};
