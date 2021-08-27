#!/usr/bin/env python3

from datetime import date
import configparser
import socket
import chess
import chess.engine
import chess.pgn

def juegaServidor():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    jugadaServidor = bytes(str(result.move), encoding="ascii")
    cliente.send(jugadaServidor)
    return str(result.move)

def juegaCliente():
    jugadaCliente = cliente.recv(10).decode("ascii")
    board.push_san(jugadaCliente)
    return jugadaCliente

def jueganBlancas(i):
    if i%2 == 1:
        return juegaCliente()
    else:
        return juegaServidor()

def jueganNegras(i):
    if i%2 == 0:
        return juegaCliente()
    else:
        return juegaServidor()

configuración = configparser.ConfigParser()
configuración.read("datos.cfg")
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("", int(configuración["conexión"]["port"])))
servidor.listen(1)
cliente, addr = servidor.accept()

engine = chess.engine.SimpleEngine.popen_uci("stockfish")

for i in range(1, 5):
    print("Jugando partida " + str(i))
    board = chess.Board()
    game = chess.pgn.Game()
    game.headers['Date'] = date.today()
    game.headers['Round'] = i
    if i%2 == 1:
        game.headers['White'] = 'Cliente'
        game.headers['Black'] = 'Servidor'
    else:
        game.headers['White'] = 'Servidor'
        game.headers['Black'] = 'Cliente'
    firstMove = True
    while not board.is_game_over():
        if firstMove:
            node = game.add_variation(chess.Move.from_uci(jueganBlancas(i)))
            firstMove = False
        else:
            node = node.add_variation(chess.Move.from_uci(jueganBlancas(i)))
        if not board.is_game_over():
            node = node.add_variation(chess.Move.from_uci(jueganNegras(i)))
    game.headers['Result'] = board.result()
    print(game, file=open("partidas.pgn", "a"), end="\n\n")

engine.quit()
cliente.close()
print("FIN")
