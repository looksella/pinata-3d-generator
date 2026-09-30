export class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  
  constructor(url: string) {
    this.url = url;
  }
  
  connect(): Promise<WebSocket> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);
      
      this.ws.onopen = () => {
        console.log('WebSocket conectado');
        resolve(this.ws!);
      };
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };
      
      this.ws.onclose = () => {
        console.log('WebSocket desconectado');
        this.ws = null;
      };
    });
  }
  
  send(data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(typeof data === 'string' ? data : JSON.stringify(data));
    } else {
      console.error('WebSocket no está conectado');
    }
  }
  
  onMessage(callback: (data: any) => void): void {
    if (this.ws) {
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          callback(data);
        } catch (error) {
          console.error('Error al parsear mensaje WebSocket:', error);
        }
      };
    }
  }
  
  close(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export const wsClient = new WebSocketClient('ws://localhost:8000/ws/generate');
