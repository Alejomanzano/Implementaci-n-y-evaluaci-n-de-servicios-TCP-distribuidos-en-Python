
import socket
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

SERVIDORES = {
    "suma": ("192.168.83.131", 50001),
    "resta": ("127.0.0.1", 50002),
    "multiplica": ("127.0.0.1", 50003),
    "divide": ("127.0.0.1", 50003)
}

OPERACIONES = {
    "suma": "suma 100 200",
    "resta": "resta 100 20",
    "multiplica": "multiplica 5 6",
    "divide": "divide 100 4"
}


def enviar_peticion(operacion):
    host, puerto = SERVIDORES[operacion]
    mensaje = OPERACIONES[operacion]

    inicio = time.perf_counter()

    try:
        with socket.create_connection(
            (host, puerto), timeout=5
        ) as cliente:
            cliente.sendall(mensaje.encode("utf-8"))
            respuesta = cliente.recv(1024).decode("utf-8")

        latencia = time.perf_counter() - inicio
        return latencia, True

    except OSError as error:
        print(f"Error de conexión: {error}")
        latencia = time.perf_counter() - inicio
        return latencia, False


def ejecutar_cliente(operacion, peticiones):
    resultados = []

    for _ in range(peticiones):
        resultados.append(enviar_peticion(operacion))

    return resultados


def ejecutar_prueba(operacion, numero_clientes, peticiones):
    print("\nIniciando prueba de carga...")
    print(f"Operacion: {operacion}")
    print(f"Clientes concurrentes: {numero_clientes}")
    print(f"Peticiones por cliente: {peticiones}")

    inicio = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=numero_clientes
    ) as executor:
        tareas = [
            executor.submit(
                ejecutar_cliente, operacion, peticiones
            )
            for _ in range(numero_clientes)
        ]

        resultados = []
        for tarea in tareas:
            resultados.extend(tarea.result())

    duracion = time.perf_counter() - inicio

    latencias = [r[0] for r in resultados]
    exitosas = sum(1 for r in resultados if r[1])
    errores = len(resultados) - exitosas

    throughput = exitosas / duracion if duracion > 0 else 0

    print("\n--- RESULTADOS ---")
    print(f"Duracion total: {duracion:.3f} segundos")
    print(f"Peticiones totales: {len(resultados)}")
    print(f"Peticiones exitosas: {exitosas}")
    print(f"Errores: {errores}")
    print(f"Throughput: {throughput:.2f} operaciones/segundo")

    if latencias:
        print(
            "Latencia media: "
            f"{statistics.mean(latencias) * 1000:.2f} ms"
        )
        print(
            "Latencia maxima: "
            f"{max(latencias) * 1000:.2f} ms"
        )


if __name__ == "__main__":
    print("=== PRUEBA DE CARGA ===")

    operacion = input(
        "Operacion (suma, resta, multiplica, divide): "
    ).strip().lower()

    if operacion not in SERVIDORES:
        print("Operacion no valida.")
        raise SystemExit(1)

    try:
        clientes = int(input("Numero de clientes concurrentes: "))
        peticiones = int(input("Peticiones por cliente: "))

        if clientes < 1 or peticiones < 1:
            raise ValueError

    except ValueError:
        print("Introduce numeros enteros mayores que cero.")
        raise SystemExit(1)

    ejecutar_prueba(operacion, clientes, peticiones)
