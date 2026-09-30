import React from 'react';
import { useStore } from '../store/useStore';

export const StyleSelector: React.FC = () => {
  const { selectedStyle, setSelectedStyle } = useStore();

  const styles = [
    {
      id: 'fiel',
      name: 'Fiel al original',
      description: 'Preserva la forma, proporciones y detalles del objeto original',
      icon: '🎯'
    },
    {
      id: 'tradicional',
      name: 'Estilizado tradicional mexicano',
      description: 'Transforma el objeto en una estética de piñata tradicional mexicana',
      icon: '🎊'
    }
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-amber-800 mb-4">Modo de Estilo</h2>
      <div className="space-y-3">
        {styles.map((style) => (
          <button
            key={style.id}
            onClick={() => setSelectedStyle(style.id)}
            className={`w-full p-4 rounded-lg border-2 transition-all text-left ${
              selectedStyle === style.id
                ? 'border-amber-500 bg-amber-50'
                : 'border-gray-200 hover:border-amber-300'
            }`}
          >
            <div className="flex items-start gap-3">
              <span className="text-2xl">{style.icon}</span>
              <div>
                <h3 className="font-medium text-gray-800">{style.name}</h3>
                <p className="text-sm text-gray-500 mt-1">{style.description}</p>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};
