from grafo import Grafo

def add_vertice(self, u):
    self.vertices.add(u)

def add_vertice_req(self, u):
    self.add_vertice(u)
    self.vertices_req.add(u)

def add_aresta(self, u, v, peso):
    self.add_vertice(u)
    self.add_vertice(v)
    aresta = tuple(sorted((u, v)))
    if aresta not in self.arestas:
        self.arestas[aresta] = []
    self.arestas[aresta].append(peso)

def add_aresta_req(self, u, v, peso):
    self.add_aresta(u, v, peso)
    aresta = tuple(sorted((u, v)))
    if aresta not in self.arestas_req:
        self.arestas_req[aresta] = peso

def add_arco(self, u, v, peso):
    self.add_vertice(u)
    self.add_vertice(v)
    arco = (u, v)
    if arco not in self.arcos:
        self.arcos[arco] = []
    self.arcos[arco].append(peso)

def add_arco_req(self, u, v, peso):
    self.add_arco(u, v, peso)
    arco = (u, v)
    if arco not in self.arcos_req:
        self.arcos_req[arco] = peso 