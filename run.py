import time
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

from MiniMax import minimax

from Board2 import Board2
from Board3 import Board3
from Board4 import Board4 as Board

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