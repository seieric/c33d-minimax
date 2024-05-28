import time
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import uuid

from Board2 import Board2
from Board3 import Board3 as Board

# ボードの状態と手番のプレイヤーを受け取り、最適な手を返したい
def minimax(board, player, depth, alpha=-1, beta=1, graph=None, parent=None):
  score = board.score()
  if score is not None:
    return score

  moves = board.get_possible_moves()
  if player:
    best = -5
    # 勝てる手がある場合はその手を選ぶ
    for move in moves:
      board.make_move(move, player)
      score = board.score()
      board.undo_move(move, player)
      if score == 1:
        #print("MAX WINNING MOVE")
        node_id = uuid.uuid1()
        if graph is not None:
          graph.add_node(node_id, data=move)
          if parent is not None:
            graph.add_edge(parent, node_id)
        return 1
    # 相手の勝ち手を防ぐ
    for move in moves:
      board.make_move(move, False)
      score = board.score()
      board.undo_move(move, False)
      if score == -1:
        #print("MAX BLOCKING MOVE")
        node_id = uuid.uuid1()
        if graph is not None:
          graph.add_node(node_id, data=move)
          if parent is not None:
            graph.add_edge(parent, node_id)
        board.make_move(move, player)
        value = minimax(board, not player, depth + 1, alpha, beta, graph, node_id)
        board.undo_move(move, player)
        return value
    # それ以外の手を試す
    for move in moves:
      node_id = uuid.uuid1()
      if graph is not None:
        graph.add_node(node_id, data=move)
        if parent is not None:
          graph.add_edge(parent, node_id)
      board.make_move(move, player)
      best = max(best, minimax(board, not player, depth + 1, alpha, beta, graph, node_id))
      board.undo_move(move, player)
      alpha = max(alpha, best)
      if alpha >= beta:
        return best
    return best
  else:
    best = 5
    for move in moves:
      board.make_move(move, player)
      score = board.score()
      board.undo_move(move, player)
      if score == -1:
        #print("MIN WINNING MOVE")
        node_id = uuid.uuid1()
        if graph is not None:
          graph.add_node(node_id, data=move)
          if parent is not None:
            graph.add_edge(parent, node_id)
        return -1
    # 相手の勝ち手を防ぐ
    for move in moves:
      board.make_move(move, not player)
      score = board.score()
      board.undo_move(move, not player)
      if score == 1:
        #print("MIN BLOCKING MOVE")
        node_id = uuid.uuid1()
        if graph is not None:
          graph.add_node(node_id, data=move)
          if parent is not None:
            graph.add_edge(parent, node_id)
        board.make_move(move, player)
        value = minimax(board, not player, depth + 1, alpha, beta, graph, node_id)
        board.undo_move(move, player)
        return value
    for move in moves:
      node_id = uuid.uuid1()
      if graph is not None:
        graph.add_node(node_id, data=move)
        if parent is not None:
          graph.add_edge(parent, node_id)
      board.make_move(move, player)
      best = min(best, minimax(board, not player, depth + 1, alpha, beta, graph, node_id))
      board.undo_move(move, player)
      beta = min(beta, best)
      if alpha >= beta:
        return best
    return best

def calculate():
    board = Board(randomize=True)
    graph = nx.DiGraph()
    graph.add_node("ROOT", data=(-1, -1, -1))
    # TrueならMAX, FalseならMIN
    current_player = True
    score = minimax(board, current_player, 0, graph=graph, parent="ROOT")
    total_nodes = len(graph.nodes)-1
    return score, total_nodes, graph

def draw_graph(graph):
    pos = graphviz_layout(graph, prog="dot")
    labels = {n: "({},{},{})".format(d['data'][0], d['data'][1], d['data'][2]) for n, d in graph.nodes(data=True)}
    plt.figure(1,figsize=(8,6)) 
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=25, node_color='lightblue', font_size=5)
    plt.show()

def main():
  nodes = []
  times = []
  for i in range(1):
    start = time.time()
    score, total_nodes, graph = calculate()
    end = time.time()
    nodes.append(total_nodes)
    times.append(end - start)
    print("GAME No.", i)
    print("Best score:", score)
    print("Total nodes:", total_nodes)
    print("Time:", times[-1], "s")
    print("")
    draw_graph(graph)
  with open("result_c33d.csv", "w") as f:
    f.write("nodes,time\n")
    for i in range(len(nodes)):
      f.write(str(nodes[i]) + "," + str(times[i]) + "\n") 

if __name__ == '__main__':
  main()