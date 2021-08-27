#!/usr/bin/env python3

import configparser
import socket
import chess
import chess.engine

def juegaCliente():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    jugadaCliente = bytes(str(result.move), encoding="ascii")
    obj.send(jugadaCliente)

def juegaServidor():
    recibido = obj.recv(10).decode("ascii")
    board.push_san(recibido)

def juega(turno):
    if turno%2 == 1:
        juegaCliente()
    else:
        juegaServidor()
    turno += 1
    return turno

configuración = configparser.ConfigParser()
configuración.read("datos.cfg")
engine = chess.engine.SimpleEngine.popen_uci("stockfish")
host = configuración["conexión"]["host"]
port = int(configuración["conexión"]["port"])
obj = socket.socket()
obj.connect((host, port))
print("Conectado al servidor")

for i in range(1, 5):
    board = chess.Board()
    turno = i
    while not board.is_game_over():
        turno = juega(turno)
        if not board.is_game_over():
            turno = juega(turno)

engine.quit()
obj.close()
print("FIN")