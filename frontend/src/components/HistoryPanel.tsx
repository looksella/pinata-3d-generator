import React, { useEffect, useState } from 'react';
import { useStore } from '../store/useStore';
import { api } from '../utils/api';

export const HistoryPanel: React.FC = () => {
  const { history, setHistory, setModelUrl } = useStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const historyData = await api.getHistory();
      setHistory(historyData);
    } catch (error) {
      console.error('Error al cargar historial:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenProject = (project: any) => {
    setModelUrl(`/outputs/${project.model_path.split('/').pop()}`);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-amber-800">Historial de Proyectos</h2>
        <button
          onClick={loadHistory}
          className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
        >
          Actualizar
        </button>
      </div>
      
      {loading ? (
        <div className="flex items-center justify-center py-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-amber-500"></div>
        </div>
      ) : history.length === 0 ? (
        <p className="text-gray-500 text-center py-4">No hay proyectos guardados</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {history.map((project, index) => (
            <div
              key={index}
              onClick={() => handleOpenProject(project)}
              className="border border-gray-200 rounded-lg p-3 cursor-pointer hover:border-amber-300 transition-all"
            >
              <img
                src={`/outputs/${project.thumbnail_path.split('/').pop()}`}
                alt={project.name}
                className="w-full h-24 object-cover rounded-lg mb-2"
              />
              <h3 className="font-medium text-gray-800 text-sm truncate">{project.name}</h3>
              <p className="text-xs text-gray-500">{new Date(project.created_at).toLocaleDateString('es-ES')}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
