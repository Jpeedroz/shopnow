# ShopNow - Teste de carga com o ab
import subprocess

total_acessos = 5000
simultaneos = [50, 100, 200, 500]


def pegar_numero(saida, texto):
    for linha in saida.splitlines():
        if linha.startswith(texto):
            depois_dos_dois_pontos = linha.split(':')[1]
            return depois_dos_dois_pontos.split()[0]
    return 'erro'


print('=' * 50)
print(f'{"Simultâneos":^12}|{"Falhas":^8}|{"Req/s":^10}|{"Tempo médio (ms)":^18}')
print('=' * 50)

for c in simultaneos:
    comando = f'ab -r -n {total_acessos} -c {c} http://127.0.0.1:8080/'
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    saida = resultado.stdout

    falhas = pegar_numero(saida, 'Failed requests')
    req_s = pegar_numero(saida, 'Requests per second')
    tempo = pegar_numero(saida, 'Time per request')

    print(f'{c:^12}|{falhas:^8}|{req_s:^10}|{tempo:^18}')

print('=' * 50)
