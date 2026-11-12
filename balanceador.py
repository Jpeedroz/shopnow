# ShopNow - Balanceador de carga
import sys
import time
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

servidores = ['http://127.0.0.1:8001',
              'http://127.0.0.1:8002',
              'http://127.0.0.1:8003']
pesos = [3, 2, 1]
fora_do_ar = []

if len(sys.argv) > 1:
    algoritmo = sys.argv[1]
else:
    algoritmo = 'roundrobin'

fila = []
if algoritmo == 'ponderado':
    for i in range(len(servidores)):
        for vez in range(pesos[i]):
            fila.append(servidores[i])
else:
    fila = servidores.copy()

posicao = 0


def proximo_servidor():
    global posicao
    servidor = fila[posicao % len(fila)]
    posicao += 1
    return servidor


def marcar_fora(servidor):
    if servidor not in fora_do_ar:
        fora_do_ar.append(servidor)
        print(f'FALHA: {servidor} caiu')


def health_check():
    while True:
        for servidor in servidores:
            try:
                urllib.request.urlopen(servidor, timeout=1)
                if servidor in fora_do_ar:
                    fora_do_ar.remove(servidor)
                    print(f'VOLTOU: {servidor}')
            except Exception:
                marcar_fora(servidor)
        time.sleep(2)


class Balanceador(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(404)
            self.end_headers()
            return

        escolhido = proximo_servidor()
        tentativas = [escolhido] + servidores

        for servidor in tentativas:
            if servidor in fora_do_ar:
                continue
            try:
                resposta = urllib.request.urlopen(servidor + self.path, timeout=3)
                conteudo = resposta.read()
            except Exception:
                marcar_fora(servidor)
                continue

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('X-Servidor', resposta.headers['X-Servidor'])
            self.end_headers()
            self.wfile.write(conteudo)
            return

        self.send_response(503)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('<h1>Nenhum servidor disponível</h1>'.encode('utf-8'))

    def log_message(self, *args):
        pass


threading.Thread(target=health_check, daemon=True).start()

print(f'Balanceador em http://localhost:8080 ({algoritmo})')
ThreadingHTTPServer.request_queue_size = 1024
ThreadingHTTPServer(('localhost', 8080), Balanceador).serve_forever()
