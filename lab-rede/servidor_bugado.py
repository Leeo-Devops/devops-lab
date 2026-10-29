import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8888))
server.listen(5)

print("Servidor rodando na porta 8888. Ele NÃO fecha as conexões!")
print("Para testar, em outro terminal rode: for i in {1..10}; do curl http://127.0.0.1:8888 & done")

while True:
    conn, addr = server.accept()
    print(f"Conexao recebida de {addr} - NAO vou fechar o socket!")
    conn.send(b"HTTP/1.1 200 OK\r\n\r\nVazando CLOSE_WAIT...")
    # BUG INTENCIONAL: falta o conn.close() aqui!
