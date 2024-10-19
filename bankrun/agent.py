import random

pa = 0.5
pb = 0.05
pc = 0.75
pd = 0.2
pe = 0.9

class Agent:
  def __init__(self, id, social_network):
      self.id = id
      self.social_network = social_network
      self.balance = 0
      self.heard = 0
      self.withdrawn = False

  def set_balance(self, amount):
    self.balance = amount

  def withdraw(self):
    self.social_network.withdraw(self.balance)
    self.emit('I have withdrawn money from the bank')
    self.withdrawn = True

  def emit(self, signal):
    self.social_network.emit(self, signal)

  # When an agent first receives a signal of 'I have heard that someone is withdrawing money from the bank', it will have a probability of p_a to spread the signal to its neighbors. If the agent has already heard the signal, it will not spread it.
  # Whenever an agent receives a signal of 'I have heard that someone is withdrawing money from the bank', it will have a probability of p_b to withdraw money from the bank.
  # Whenever an agent receives a signal of 'I have withdrawn money from the bank', it will have a probability of p_c to spread the signal 'I have heard that someone is withdrawing money from the bank' to its neighbors.
  # Whenever an agent receives a signal of 'I have withdrawn money from the bank', it will have a probability of p_d to withdraw money from the bank.
  # Whenever an agent withdraws money from the bank, it will have a probability of p_e to spread the signal 'I have withdrawn money from the bank' to its neighbors.
  def receive(self, signal):
    if self.withdrawn:
      return
    print(f'Agent {self.id} received signal: {signal}, heard: {self.heard}')
    if signal == 'I have heard that someone is withdrawing money from the bank':
      if self.heard == 0:
        if random.random() < pa:
          self.emit(signal)
      if random.random() < pb:
        self.withdraw()
      self.heard += 1
    elif signal == 'I have withdrawn money from the bank':
      if random.random() < pc:
        self.emit(signal)
      if random.random() < pd:
        self.withdraw()