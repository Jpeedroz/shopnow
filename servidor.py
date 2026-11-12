# ShopNow - Servidor do site
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

porta = int(sys.argv[1])
nome = f'Servidor {porta - 8000}'

produtos = ['Smartphone X10 - R$ 1899,90',
            'Notebook Pro 14 - R$ 4599,00',
            'Fone Bluetooth - R$ 199,90',
            'Smart TV 50 - R$ 2399,00']


def montar_pagina():
    html = '<h1>ShopNow - Black Friday</h1>'
    html += f'<h2>Atendido por: {nome}</h2>'
    html += '<ul>'
    for produto in produtos:
        html += f'<li>{produto}</li>'
    html += '</ul>'
    return html


class Site(BaseHTTPRequestHandler):
    def do_GET(self):
        pagina = montar_pagina()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('X-Servidor', nome)
        self.end_headers()
        self.wfile.write(pagina.encode('utf-8'))

    def log_message(self, *args):
        pass


print(f'{nome} em http://localhost:{porta}')
ThreadingHTTPServer.request_queue_size = 1024
ThreadingHTTPServer(('localhost', porta), Site).serve_forever()
