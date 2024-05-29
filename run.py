import time
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
from multiprocessing import Pool

from MiniMax import minimax
from MiniMaxSimple import minimax_simple

from Board2 import Board2
from Board3 import Board3 as Board
from Board4 import Board4

def _calculate():
    board = Board(randomize=True)
    graph = nx.DiGraph()
    graph.add_node("ROOT", data=(-1, -1, -1))
    # TrueならMAX, FalseならMIN
    current_player = True
    score = minimax(board, current_player, 0, graph=graph, parent="ROOT")
    total_nodes = len(graph.nodes)-1
    return score, total_nodes, graph

def  calculate(i):
  start = time.time()
  score, total_nodes, graph = _calculate()
  end = time.time()
  time_taken = end - start
  print("GAME No.", i)
  print("Best score:", score)
  print("Total nodes:", total_nodes)
  print("Time:", time_taken, "s")
  print("")
  #draw_graph(graph)
  return total_nodes, time_taken

def draw_graph(graph):
    pos = graphviz_layout(graph, prog="dot")
    labels = {n: "({},{},{})".format(d['data'][0], d['data'][1], d['data'][2]) for n, d in graph.nodes(data=True)}
    plt.figure(1,figsize=(8,6)) 
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=25, node_color='lightblue', font_size=5)
    plt.show()

def main():
  nodes = []
  times = []
  with Pool(10) as p:
    for i in range(10):
      results = p.map(calculate, range(10))
      nodes_batch, times_batch = zip(*results)
      nodes.extend(nodes_batch)
      times.extend(times_batch)
  with open("results.csv", "w") as f:
    f.write("nodes,time\n")
    for i in range(len(nodes)):
      f.write(str(nodes[i]) + "," + str(times[i]) + "\n") 

if __name__ == '__main__':
  main()