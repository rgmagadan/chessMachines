#!/usr/bin/env python3

import configparser
import socket
import chess
import chess.engine

configuración = configparser.ConfigParser()
configuración.read("datos.cfg")
engine = chess.engine.SimpleEngine.popen_uci("stockfish")
board = chess.Board()
host = configuración["conexión"]["host"]
port = int(configuración["conexión"]["port"])
obj = socket.socket()
obj.connect((host, port))
print("Conectado al servidor")

while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    jugadaCliente = bytes(str(result.move), encoding="ascii")
    obj.send(jugadaCliente)
    if not board.is_game_over():
        recibido = obj.recv(10).decode("ascii")
        board.push_san(recibido)

engine.quit()
obj.close()
print("Adiós")