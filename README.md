# ShopNow — Balanceador de Carga

Sistema de balanceamento de carga em Python para o e-commerce ShopNow. Três instâncias do site rodam atrás de um balanceador, que distribui os acessos com os algoritmos Round Robin ou Ponderado. Se um servidor cai, o acesso vai para outro, e o health check percebe quando ele volta.

## Fluxo

```
Cliente ──> Balanceador (8080) ──┬──> Servidor 1 (8001)
                                 ├──> Servidor 2 (8002)
                                 └──> Servidor 3 (8003)
```

1. O cliente acessa o balanceador.
2. O balanceador escolhe o servidor pelo algoritmo.
3. O servidor devolve a página, que chega ao cliente.

## Como rodar

Requisitos: Python 3 e Apache Benchmark (`sudo apt install apache2-utils`).

Em 4 terminais:

```
python3 servidor.py 8001
python3 servidor.py 8002
python3 servidor.py 8003
python3 balanceador.py roundrobin    # ou: ponderado
```

Acesse http://127.0.0.1:8080

Teste de carga:

```
ab -n 5000 -c 100 http://127.0.0.1:8080/
python3 teste_carga.py
```
