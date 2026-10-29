import time
import os

print(f"PID: {os.getpid()} - Iniciando consumo de RAM...")
blocos = []
try:
    while True:
        # Aloca 50MB por vez
        blocos.append(bytearray(50 * 1024 * 1024))
        print(f"Alocado: {len(blocos) * 50} MB", flush=True)
        time.sleep(0.1)
except Exception as e:
    print(f"Erro: {e}")
