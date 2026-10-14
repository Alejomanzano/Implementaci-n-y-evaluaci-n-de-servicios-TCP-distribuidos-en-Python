import socket
HOST = "127.0.0.1"
PORT = 50000

while True:
    mensaje = input("Operacion (ej. sum 3 4) o 'salir': "
                    ).strip() 
    
    if mensaje.lower() == "salir":
        break
    
    try:
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as cliente:
            
            cliente.settimeout(3)
            cliente.connect((HOST, PORT))
            cliente.sendall(mensaje.encode("utf-8"))
            
            respuesta = cliente.recv(1024).decode("utf-8")
            
            if respuesta:
                print("respuesta del servidor:", respuesta)
            else: 
               print("El servidor cerro la conexion sin responder.")
            
    except socket.timeout:
        print("Tiempo agotado: el servidor no respondio en 3 segundos")
    except OSError as error:
        print("Error de conexion:", error)