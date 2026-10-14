import socket
import threading

HOST = "127.0.0.1"
POST = 50001

def atender_cliente(conexion, direccion):
    with conexion:
        print(f"Cliente conectado: {direccion}")
        
        datos = conexion.recv(1024)
        
        if not datos:
            return
        
        mensaje = datos.decode("utf-8").strip()
        partes = mensaje.split()
        
        if len(partes) != 3 or partes[0].lower() != "suma":
            respuesta = "Error: formato esperando: suma numero1 numero2"
        else:
            try:
                a = float(partes[1])
                b = float(partes[2])
                respuesta = str(a+b)
            except ValueError:
                respuesta = "Error los operandos debe ser numeros"
                
        conexion.sendall(respuesta.encode("utf-8"))
        print(f"Solicitud: {mensaje!r} -> {respuesta}")
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, POST))
    servidor.listen()
    
    print(f"El servidor de suma escuchando en {HOST}:{POST}")
    
    while True:
        conexion, direccion = servidor.accept()
        
        hilo = threading.Thread(
            target=atender_cliente,
            args=(conexion,direccion)
        )
        hilo.start()