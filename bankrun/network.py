import networkx as nx
from bankrun.agent import Agent
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pareto

class SocialNetwork:
  def __init__(self, n0, m0, t):
    self.graph = nx.Graph()
    self.agents = []
    self.size = 0
    self.total_degree = 0
    self.barabasi_albert(n0, m0, t)

    balances = pareto.rvs(1.16, 1000, size=self.size)
    for i, balance in enumerate(balances):
      self.agents[i].set_balance(balance)
    self.total_deposits = sum(balances)
    self.bankrun_threshold = 0.1 * self.total_deposits

  def add_node(self):
    agent = Agent(self.size, self)
    self.agents.append(agent)
    self.graph.add_node(self.size)
    self.size += 1
    return self.size - 1, agent

  def add_edge(self, i, j):
    self.graph.add_edge(i, j)

  def barabasi_albert(self, n0, m0, t):
    for i in range(n0):
      self.add_node()
      for j in range(i):
        self.add_edge(i, j)
    def step(self, n):
      degrees = dict(self.graph.degree())
      total_degree = sum(degrees.values())
      self.add_node()
      for j in range(m0):
        p = [degrees[k] / total_degree for k in range(n)]
        j = np.random.choice(n, p=p)
        self.add_edge(n, j)
    for _ in range(t):
      step(self, self.size)

  def render(self, seed = 13648):
    pos = nx.spring_layout(self.graph, seed=seed)

    node_colors = self.get_heard()
    node_colors = [h + 5 for h in node_colors]

    edge_colors = [self.graph[u][v]['weight'] if 'weight' in self.graph[u][v] else 0 for u, v in self.graph.edges()]

    nodes = nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, node_size=300, cmap=plt.cm.Blues)
    edges = nx.draw_networkx_edges(
      self.graph,
      pos,
      arrowstyle="->",
      arrowsize=10,
      width=4,
      edge_color=edge_colors,
      edge_cmap=plt.cm.Blues,
    )
    plt.show()
    
  def emit(self, agent, signal):
    neighbors = self.graph[agent.id]
    for neighbor, _ in neighbors.items():
      self.agents[neighbor].receive(signal)
      u, v = agent.id, neighbor
      self.graph[u][v]['weight'] = self.graph[u][v].get('weight', 0) + 1
      

  def get_heard(self):
    return [agent.heard for agent in self.agents]
  
  def withdraw(self, amount):
    self.total_deposits -= amount
    if self.total_deposits < self.bankrun_threshold:
      print('\33[31mBank run!\33[0m')

  def __str__(self):
    return str(self.adjacency)
  
if __name__ == '__main__':
  network = SocialNetwork(5, 2, 100)
  network.render()
  network.agents[0].withdraw()
  network.render()