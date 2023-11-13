# SIP_Exporter

## Description

This repository contains the SIP Exporter for Prometheus, packaged in a Docker container. The image is available on Docker Hub under the tag cristokram/sipexporter:0.0.1. The SIP Exporter enables monitoring of SIP servers through Prometheus by sending SIP OPTIONS requests and gathering metrics such as response time and SIP status code.

## Usage
### Docker

To run the SIP Exporter in a Docker container, use the following command:
```
docker run -d -p 8001:8001 cristokram/sipexporter:0.0.1
```

This will start the SIP Exporter listening on port 8001.

### Prometheus Job Configuration

To add the SIP Exporter to your Prometheus configuration, add the following job in your prometheus.yml file:
```
scrape_configs:
  - job_name: 'sip'
    static_configs:
      - targets: ['sip.kram.pro:5060']  # Reemplace con su servidor SIP objetivo
    metrics_path: '/metrics'
    params:
      module: ['UDP']  # O 'TCP' O 'TLS' según su preferencia
    scrape_interval: 15s
    scrape_timeout: 5s

```
This will configure Prometheus to make requests every 15 seconds.

----------------------------------------------------------------
## Descripción
Este repositorio contiene el SIP Exporter para Prometheus, empacado en un contenedor Docker. La imagen está disponible en Docker Hub bajo la etiqueta cristokram/sipexporter:0.0.1. El SIP Exporter permite monitorear servidores SIP a través de Prometheus, enviando peticiones SIP OPTIONS y recogiendo métricas como el tiempo de respuesta y el código de estado SIP

## Uso
### Docker 
Para ejecutar el SIP Exporter en un contenedor Docker, utilice el siguiente comando:
```
docker run -d -p 8001:8001 cristokram/sipexporter:0.0.1
```
Esto iniciará el SIP Exporter escuchando en el puerto 8001.

### Configuración del Job en Prometheus

Para añadir el SIP Exporter a su configuración de Prometheus, añada el siguiente job en su archivo prometheus.yml:
```
scrape_configs:
  - job_name: 'sip'
    static_configs:
      - targets: ['sip.kram.pro:5060']  # Reemplace con su servidor SIP objetivo
    metrics_path: '/metrics'
    params:
      module: ['UDP']  # O 'TCP' O 'TLS' según su preferencia
    scrape_interval: 15s
    scrape_timeout: 5s

```