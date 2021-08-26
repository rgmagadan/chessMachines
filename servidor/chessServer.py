#!/usr/bin/env python3

import configparser
import socket
import chess
import chess.engine
import chess.pgn

configuración = configparser.ConfigParser()
configuración.read("datos.cfg")
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser.bind(("", int(configuración["conexión"]["port"])))
ser.listen(1)
cli, addr = ser.accept()

engine = chess.engine.SimpleEngine.popen_uci("stockfish")
board = chess.Board()
game = chess.pgn.Game()
firstMove = True

while not board.is_game_over():
    jugadaCliente = cli.recv(10).decode("ascii")
    board.push_san(jugadaCliente)
    print("El cliente ha jugado " + jugadaCliente)
    if firstMove:
        node = game.add_variation(chess.Move.from_uci(jugadaCliente))
        firstMove = False
    else:
        node = node.add_variation(chess.Move.from_uci(jugadaCliente))
    if not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        jugadaServidor = bytes(str(result.move), encoding="ascii")
        cli.send(jugadaServidor)
        print("El servidor ha movido " + str(result.move))
        node = node.add_variation(chess.Move.from_uci(str(result.move)))

engine.quit()
cli.close()
print(game, file=open("partidas.pgn", "w"), end="\n\n")
print("Adiós")