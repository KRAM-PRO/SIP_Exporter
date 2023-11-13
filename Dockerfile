# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt ./
COPY sip_exporter.py ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto donde se ejecuta el exporter
EXPOSE 8001

# Comando para ejecutar el exporter
CMD ["python", "./sip_exporter.py"]
