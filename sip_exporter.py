from flask import Flask, Response, request
import socket
import ssl
import time
import uuid
import logging
import sys

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def generate_call_id():
    return str(uuid.uuid4())

def parse_response_code(response):
    try:
        status_line = response.split("\r\n")[0]
        return status_line.split(" ")[1]
    except IndexError:
        return "No se pudo obtener el código de estado"

def send_sip_options(target, module, timeout=5):
    host, port = target.split(":")
    port = int(port)
    protocol = module.upper()

    call_id = generate_call_id()

    message = f"OPTIONS sip:{host} SIP/2.0\r\n" \
              f"Via: SIP/2.0/{protocol} {host}:{port}\r\n" \
              f"From: <sip:test@{host}>\r\n" \
              f"To: <sip:{host}>\r\n" \
              f"Call-ID: {call_id}@{host}\r\n" \
              f"CSeq: 1 OPTIONS\r\n" \
              f"Content-Length: 0\r\n\r\n"

    try:
        if protocol == 'TCP' or protocol == 'TLS':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if protocol == 'TLS':
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.settimeout(timeout)
        start_time = time.time()

        if protocol == 'UDP':
            sock.sendto(message.encode(), (host, port))
        else:
            sock.connect((host, port))
            sock.sendall(message.encode())

        response = sock.recv(4096)
        elapsed_time = time.time() - start_time
        sock.close()

        response_code = parse_response_code(response.decode())
        logging.info(f"Respuesta SIP recibida: {response_code}, Tiempo: {elapsed_time} segundos")
        return response_code, elapsed_time
    except socket.timeout:
        logging.error("Error: Timeout alcanzado")
        return "408", None
    except Exception as e:
        logging.error(f"Error: {e}")
        return "500", None

@app.route('/metrics')
def metrics():
    target = request.args.get('target', '0.0.0.0:0')
    module = request.args.get('module', 'UDP')
    response_code, elapsed_time = send_sip_options(target, module)

    up = 1 if elapsed_time is not None else 0
    metrics_response = f"""
# HELP sip_up Indicador de disponibilidad del servidor SIP
# TYPE sip_up gauge
sip_up{{target="{target}", module="{module}"}} {up}
# HELP sip_response_time_seconds Tiempo de respuesta del servidor SIP
# TYPE sip_response_time_seconds gauge
sip_response_time_seconds{{target="{target}", module="{module}"}} {elapsed_time or 0}
# HELP sip_response_code Código de respuesta SIP
# TYPE sip_response_code gauge
sip_response_code{{target="{target}", module="{module}"}} {response_code or 0}
"""
    return Response(metrics_response, mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
