"""
Author: Satwik Srivastava
Date: 20-02-2021

Description:

"""

import math
import pydantic
from dataclasses import dataclass
import numpy as np
from collections import defaultdict


# GLOBAL VARIABLES
INF = float('inf')
OPERATIONS_DICT = {}


# === BASE VARIABLE CLASS === #
# @dataclass
class Node(pydantic.BaseModel):
    """A dataclass representing a base variable"""
    value: float
    name: str
    
    def __repr__(self) -> str:
        return "{} = {}".format(self.name, self.value)
    
    def __str__(self) -> str:
        return repr(self)
    
        
class Edge:
    """Class representing an edge which represents an operation from one node to another"""
    def __init__(self, value, name, local_gradients=[]) -> None:
        self.src = Node(value=value, name=name)
        self.value = value
        self.name = name
        self.local_gradients = local_gradients
        self.history = {}
        
    def __repr__(self) -> str:
        return "{} = {}".format(self.name, self.value)
    
    def __str__(self):
        return repr(self)
        
    def __add__(self, other):
        self.dest = other
        self.history['+'] = (self.src, self.dest.src)
        return add(self, other)
    
    def __mul__(self, other):
        self.dest = other
        self.history['*'] = (self.src, self.dest.src)
        return mul(self, other)
    
    def __sub__(self, other):
        self.dest = other
        self.history['-'] = (self.src, self.dest.src)
        return add(self, neg(other))

    def __truediv__(self, other):
        self.dest = other
        self.history['/'] = (self.src, self.dest.src)
        return mul(self, inv(other))
 


# === OPERATION FUNCTIONS === #  
# F = A + B
      
def add(a, b, name=None):
    """Create the variable that results from adding two variables."""
    value = a.value + b.value
    if name is None:
        name = '(' + a.name + ' + ' + b.name + ')'
    local_gradients = [(a, 1),  # the local derivative with respect to a is 1
                       (b, 1)]  # the local derivative with respect to b is 1
    
    return Edge(value, name, local_gradients)

# F = AB
def mul(a, b, name=None):
    """Create a Variable that results from multiplying two variables"""
    value = a.value * b.value
    if name is None:
        name = '(' + a.name + '*' + b.name + ')'
    local_gradients = [(a, b.value),   # the local derivative with respect to a is b.value
                       (b, a.value)]   # the local derivative with respect to b is a.value
    
    return Edge(value, name, local_gradients)


def neg(a, name=None):
    value = -1*a.value
    if name is None:
        name = '(-'+a.name+')'
    local_gradients = [(a.value, -1)]
    
    return Edge(value, name, local_gradients)

# F = 1 / A
def inv(a, name=None):
    value = 1. / a.value
    if name is None:
        name = '(1/'+a.name+')'
    local_gradients = [(a, -1 / a.value**2)]
    
    return Edge(value, name, local_gradients)


def sin(a):
    value = np.sin(a.value)
    name = 'sin(' + a.name +')'
    local_gradients = [(a, np.cos(a.value))]
    
    return Edge(value, name, local_gradients)


def exp(a):
    value = np.exp(a.value)
    name = 'exp(' + a.name + ')'
    local_gradients = [(a, value)]

    return Edge(value, name, local_gradients)


def log(a):
    value = np.log(a.value)
    name = 'log(' + a.name + ')'
    local_gradients = [(a, 1. / a.value)]
    
    return Edge(value, name, local_gradients)  

 
# === GRADIENT FUNCTION === #
#  f, a, b, c, d, e
def get_gradients(variable):
    """Compute the first derivatives of 'variables' wrt to their child variables"""
    gradients = defaultdict(lambda: 0)  # init defaultdict of zeros AS KEYS
    
    def compute_gradients(variable, path_value):
        for child, local_gradient in variable.local_gradients:
            # multiply the edges of the path
            value_of_path_to_child = path_value*local_gradient
            # add together different paths
            gradients[child] += value_of_path_to_child
            # recurse through the graph
            compute_gradients(child, value_of_path_to_child)
        
    compute_gradients(variable, path_value=1)

    return gradients
