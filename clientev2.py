import socket

SERVIDORES = {
    "suma": ("192.168.83.131", 50001),
    "resta": ("127.0.0.1", 50002),
    "multiplica": ("127.0.0.1", 50003),
    "divide": ("127.0.0.1", 50003)
}


def enviar_operacion(operacion, numero1, numero2):
    host, puerto = SERVIDORES[operacion]

    mensaje = f"{operacion} {numero1} {numero2}"

    try:
        with socket.create_connection((host, puerto), timeout=5) as cliente:
            cliente.sendall(mensaje.encode("utf-8"))
            respuesta = cliente.recv(1024).decode("utf-8")
            return respuesta

    except OSError as error:
        return f"Error de conexion con el servidor: {error}"


while True:
    mensaje = input(
        "Operacion (suma, resta, multiplica, divide) "
        "o 'salir': "
    ).strip()

    if mensaje.lower() == "salir":
        print("Cliente finalizado.")
        break

    partes = mensaje.split()

    if len(partes) != 3:
        print("Formato incorrecto. Ejemplo: suma 3 4")
        continue

    operacion = partes[0].lower()

    if operacion not in SERVIDORES:
        print("Operacion no reconocida.")
        continue

    try:
        numero1 = float(partes[1])
        numero2 = float(partes[2])
    except ValueError:
        print("Error: los operandos deben ser numeros.")
        continue

    respuesta = enviar_operacion(operacion, numero1, numero2)
    print("Respuesta del servidor:", respuesta)
