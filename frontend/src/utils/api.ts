import axios from 'axios';

const API_BASE_URL = '/api';

export const api = {
  getGpuInfo: async () => {
    const response = await axios.get(`${API_BASE_URL}/gpu-info`);
    return response.data;
  },
  
  uploadImage: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  
  preprocessImage: async (filePath: string) => {
    const response = await axios.post(`${API_BASE_URL}/preprocess`, null, {
      params: { file_path: filePath },
    });
    return response.data;
  },
  
  editModel: async (modelPath: string, editParams: any) => {
    const response = await axios.post(`${API_BASE_URL}/edit`, editParams, {
      params: { model_path: modelPath },
    });
    return response.data;
  },
  
  exportModel: async (modelPath: string, format: string, outputPath?: string) => {
    const response = await axios.post(`${API_BASE_URL}/export`, null, {
      params: {
        model_path: modelPath,
        format: format,
        output_path: outputPath,
      },
    });
    return response.data;
  },
  
  openInBlender: async (modelPath: string, pinataType: string, materials: any) => {
    const response = await axios.post(`${API_BASE_URL}/open-in-blender`, null, {
      params: {
        model_path: modelPath,
        pinata_type: pinataType,
        materials: JSON.stringify(materials),
      },
    });
    return response.data;
  },
  
  getHistory: async () => {
    const response = await axios.get(`${API_BASE_URL}/history`);
    return response.data;
  },
};
