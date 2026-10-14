
import socket

HOST = "127.0.0.1"
PORT = 50000


def calcular(mensaje):
    partes = mensaje.strip().split()

    if len(partes) != 3:
        return "Error: formato esperado: operacion numero1 numero2"

    operacion = partes[0].lower()

    try:
        a = float(partes[1])
        b = float(partes[2])
    except ValueError:
        return "Error: los operandos deben ser numeros"

    if operacion == "suma":
        resultado = a + b
    elif operacion == "resta":
        resultado = a - b
    elif operacion == "multiplica":
        resultado = a * b
    elif operacion == "divide":
        if b == 0:
            return "Error: division por cero"
        resultado = a / b
    else:
        return "Error: operacion no reconocida"

    return str(resultado)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        conexion, direccion = servidor.accept()

        with conexion:
            print(f"Cliente conectado: {direccion}")

            datos = conexion.recv(1024)

            if datos:
                mensaje = datos.decode("utf-8")
                respuesta = calcular(mensaje)
                conexion.sendall(respuesta.encode("utf-8"))
                print(f"Solicitud: {mensaje!r} -> {respuesta}")
