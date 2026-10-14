
import socket
import threading

HOST = "0.0.0.0"
PORT = 50003


def atender_cliente(conexion, direccion):
    print(f"Cliente conectado: {direccion}")

    try:
        with conexion:
            mensaje = conexion.recv(1024).decode("utf-8").strip()
            partes = mensaje.split()

            if len(partes) != 3:
                conexion.sendall(b"Error: formato incorrecto")
                return

            operacion = partes[0].lower()

            try:
                numero1 = float(partes[1])
                numero2 = float(partes[2])
            except ValueError:
                conexion.sendall(b"Error: operandos invalidos")
                return

            if operacion == "multiplica":
                resultado = numero1 * numero2
            elif operacion == "divide":
                if numero2 == 0:
                    conexion.sendall(b"Error: division por cero")
                    return
                resultado = numero1 / numero2
            else:
                conexion.sendall(b"Error: operacion no soportada")
                return

            respuesta = str(resultado)
            conexion.sendall(respuesta.encode("utf-8"))
            print(f"{mensaje} = {respuesta}")

    except OSError as error:
        print(f"Error de conexion: {error}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"Servidor de multiplicacion y division escuchando en {HOST}:{PORT}")

    while True:
        conexion, direccion = servidor.accept()
        hilo = threading.Thread(
            target=atender_cliente,
            args=(conexion, direccion),
            daemon=True
        )
        hilo.start()
