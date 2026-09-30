FROM node:18-alpine

WORKDIR /app

# Copiar package.json
COPY package.json .

# Instalar dependencias
RUN npm install

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 5173

# Comando para ejecutar
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
