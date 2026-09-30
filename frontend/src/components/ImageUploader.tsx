import React, { useRef, useState } from 'react';
import { useStore } from '../store/useStore';
import { api } from '../utils/api';

export const ImageUploader: React.FC = () => {
  const { uploadedImage, setUploadedImage, processedImage, setProcessedImage, setMaskPath } = useStore();
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileUpload(e.target.files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    // Validar tipo de archivo
    if (!file.type.startsWith('image/')) {
      setError('El archivo debe ser una imagen (JPG, PNG, WEBP)');
      return;
    }
    
    // Validar tamaño (máximo 20MB)
    if (file.size > 20 * 1024 * 1024) {
      setError('La imagen no debe superar los 20MB');
      return;
    }
    
    setError(null);
    setUploading(true);
    
    try {
      // Subir imagen
      const result = await api.uploadImage(file);
      const imageUrl = `/uploads/${result.filename}`;
      setUploadedImage(imageUrl);
      
      // Procesar imagen
      setProcessing(true);
      const processed = await api.preprocessImage(result.file_path);
      setProcessedImage(`/outputs/${processed.processed_image_path.split('/').pop()}`);
      setMaskPath(`/outputs/${processed.mask_path.split('/').pop()}`);
      
    } catch (err) {
      setError('Error al procesar la imagen. Inténtalo de nuevo.');
      console.error(err);
    } finally {
      setUploading(false);
      setProcessing(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-amber-800 mb-4">Imagen de Referencia</h2>
      
      {!uploadedImage ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
            dragging ? 'border-amber-500 bg-amber-50' : 'border-gray-300 hover:border-amber-300'
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            accept="image/jpeg,image/png,image/webp"
            className="hidden"
          />
          
          {uploading ? (
            <div className="flex flex-col items-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
              <p className="mt-2 text-gray-600">Subiendo imagen...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p className="mt-2 text-gray-600">Arrastra una imagen aquí o haz clic para seleccionar</p>
              <p className="text-xs text-gray-400 mt-1">JPG, PNG, WEBP (máximo 20MB)</p>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <div className="relative">
            <img
              src={uploadedImage}
              alt="Imagen original"
              className="w-full rounded-lg"
            />
            <button
              onClick={() => {
                setUploadedImage(null);
                setProcessedImage(null);
                setMaskPath(null);
              }}
              className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          {processing && (
            <div className="flex items-center justify-center p-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-amber-500"></div>
              <p className="ml-2 text-gray-600">Procesando imagen...</p>
            </div>
          )}
          
          {processedImage && (
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Imagen procesada</h3>
              <img
                src={processedImage}
                alt="Imagen procesada"
                className="w-full rounded-lg border border-gray-200"
              />
            </div>
          )}
        </div>
      )}
      
      {error && (
        <div className="mt-4 p-3 bg-red-50 text-red-600 rounded-lg text-sm">
          {error}
        </div>
      )}
    </div>
  );
};
