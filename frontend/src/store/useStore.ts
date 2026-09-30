import { create } from 'zustand';

interface GpuInfo {
  available: boolean;
  name: string | null;
  total_memory_mb: number;
  free_memory_mb: number;
  driver_version: string | null;
  recommended_model: string | null;
}

interface PinataState {
  currentStep: number;
  uploadedImage: string | null;
  processedImage: string | null;
  maskPath: string | null;
  selectedStyle: string;
  selectedType: string;
  bodyMaterial: string;
  fringeMaterial: string;
  finishMaterial: string;
  modelUrl: string | null;
  viewMode: string;
  gpuInfo: GpuInfo | null;
  history: any[];
  
  setCurrentStep: (step: number) => void;
  setUploadedImage: (image: string | null) => void;
  setProcessedImage: (image: string | null) => void;
  setMaskPath: (path: string | null) => void;
  setSelectedStyle: (style: string) => void;
  setSelectedType: (type: string) => void;
  setBodyMaterial: (material: string) => void;
  setFringeMaterial: (material: string) => void;
  setFinishMaterial: (material: string) => void;
  setModelUrl: (url: string | null) => void;
  setViewMode: (mode: string) => void;
  setGpuInfo: (info: GpuInfo | null) => void;
  setHistory: (history: any[]) => void;
}

export const useStore = create<PinataState>((set) => ({
  currentStep: 1,
  uploadedImage: null,
  processedImage: null,
  maskPath: null,
  selectedStyle: 'fiel',
  selectedType: 'escultura-3d',
  bodyMaterial: 'crepe',
  fringeMaterial: 'medio',
  finishMaterial: 'mate',
  modelUrl: null,
  viewMode: 'textured',
  gpuInfo: null,
  history: [],
  
  setCurrentStep: (step) => set({ currentStep: step }),
  setUploadedImage: (image) => set({ uploadedImage: image }),
  setProcessedImage: (image) => set({ processedImage: image }),
  setMaskPath: (path) => set({ maskPath: path }),
  setSelectedStyle: (style) => set({ selectedStyle: style }),
  setSelectedType: (type) => set({ selectedType: type }),
  setBodyMaterial: (material) => set({ bodyMaterial: material }),
  setFringeMaterial: (material) => set({ fringeMaterial: material }),
  setFinishMaterial: (material) => set({ finishMaterial: material }),
  setModelUrl: (url) => set({ modelUrl: url }),
  setViewMode: (mode) => set({ viewMode: mode }),
  setGpuInfo: (info) => set({ gpuInfo: info }),
  setHistory: (history) => set({ history }),
}));
