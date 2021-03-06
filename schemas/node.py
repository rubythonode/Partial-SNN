from .model import Model
from .node_types import node_types

import math

class Node:
  def __init__(self, node_type: int, x: int, y: int, z: int = 0, input: int = None):
    self.axon: float = 1.5
    self.threshold: float = -52.0
    self.voltage: float = -65.0
    self.theta: float = 0.05
    self.refrac: int = 0
    self.decay: float = 100.0
    self.x: int = x
    self.y: int = y
    self.z: int = z
    self.type: int = node_type
    self.others: list = []
    self.next: int = 0

  def __repr__(self):
    coord = f'({self.x}, {self.y}, {self.z})'
    return f'<Node {node_types.get_repr(self.type)}, a: {self.axon}, v: {self.voltage}, c: {coord}>'

  def update_ref(self, nodes: list):
    self.others = [
      node
      for node in nodes
      if (
        node.x != self.x and
        node.y != self.y and
        node.type != node_types.INPUT
      )
    ]

  def get_dist(self, target):
    return math.sqrt(
      (self.x - target.x) ** 2 +
      (self.y - target.y) ** 2
    )

  def spike(self, time = 0):
    if self.type == node_types.HIDDEN:
      if self.refrac:
        self.refrac -= 1
        return False
      else:
        self.refrac = 5
    elif self.type == node_types.INPUT:
      self.next = time + 1

    print(f'[*] ⚡️ Spiked {self}!')
    for node in self.others:
      if self.get_dist(node) < self.axon:
        node.voltage += self.theta * self.get_dist(node)
        if node.voltage > node.threshold:
          node.axon += 0.15
          node.x = node.x + (self.x - node.x) * 0.5
          node.y = node.y + (self.y - node.y) * 0.5
          node.next = time + 1
          node.threshold -= node.decay
          if node.type == node_types.OUTPUT:
            print(f'[*] 🔥 Fired Output node {node}!')
            return True
        else:
          if node.axon - 0.15 > 1:
            node.axon -= 0.15
            node.x = node.x + (self.x - node.x) * -0.015
            node.y = node.y + (self.y - node.y) * -0.015
    return False
