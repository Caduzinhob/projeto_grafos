def densidade_grafo(self):
    V = len(self.vertices)
    if V <= 1:
        return 0.0
    total_conexoes = len(self.arestas) + len(self.arcos)
    max_conexoes = V * (V - 1)
    return total_conexoes / max_conexoes

def calcular_graus(self):
    graus = {v: 0 for v in self.vertices}
    for (u, v), _ in self.arestas.items():
        graus[u] += 1
        graus[v] += 1
    for (u, v), _ in self.arcos.items():
        graus[u] += 1  # saída
        graus[v] += 1  # entrada
    return graus

def grau_minimo(self):
    graus = self.calcular_graus()
    return min(graus.values()) if graus else 0

def grau_maximo(self):
    graus = self.calcular_graus()
    return max(graus.values()) if graus else 0

def floyd_warshall_intermediacao(self):
    vertices = sorted(self.vertices)
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    INF = float('inf')

    dist = [[INF] * n for _ in range(n)]
    pred = [[-1] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    # processa arestas
    for (u, v), pesos in self.arestas.items():
        i, j = idx[u], idx[v]
        peso = min(pesos)
        if peso < dist[i][j]:
            dist[i][j] = dist[j][i] = peso
            pred[i][j] = i
            pred[j][i] = j

    # processa arestas requeridas
    for (u, v), peso in self.arestas_req.items():
        i, j = idx[u], idx[v]
        if peso < dist[i][j]:
            dist[i][j] = dist[j][i] = peso
            pred[i][j] = i
            pred[j][i] = j

    # processa arcos
    for (u, v), pesos in self.arcos.items():
        i, j = idx[u], idx[v]
        peso = min(pesos)
        if peso < dist[i][j]:
            dist[i][j] = peso
            pred[i][j] = i

    # processa arcos requeridos
    for (u, v), peso in self.arcos_req.items():
        i, j = idx[u], idx[v]
        if peso < dist[i][j]:
            dist[i][j] = peso
            pred[i][j] = i

    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]

    # calculo da intermediação
    intermed = {v: 0 for v in self.vertices}
    for s in range(n):
        for t in range(n):
            if s == t:
                continue
            caminho = []
            atual = t
            while atual != s and atual != -1:
                caminho.append(atual)
                atual = pred[s][atual]
            if atual == s:
                caminho.append(s)
                for v in caminho[1:-1]:  # ignora s e t
                    intermed[vertices[v]] += 1

    return dist, intermed

def caminho_medio(self):
    dist, _ = self.floyd_warshall_intermediacao()
    n = len(self.vertices)
    total = 0
    count = n * (n - 1)
    for i in range(n):
        for j in range(n):
            if i != j:
                total += dist[i][j]
    return total / count if count > 0 else 0

def diametro(self):
    dist, _ = self.floyd_warshall_intermediacao()
    max_dist = 0
    n = len(self.vertices)
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf'):
                max_dist = max(max_dist, dist[i][j])
    return max_dist 

def componentes_conectados(self):
    visitados = set()
    componentes = 0

    vizinhos = {v: set() for v in self.vertices}
    for (u, v), _ in self.arestas.items():
        vizinhos[u].add(v)
        vizinhos[v].add(u)
    for (u, v), _ in self.arestas_req.items():
        vizinhos[u].add(v)
        vizinhos[v].add(u)

    for v in self.vertices:
        if v not in visitados:
            componentes += 1
            pilha = [v]
            while pilha:
                atual = pilha.pop()
                if atual not in visitados:
                    visitados.add(atual)
                    pilha.extend(n for n in vizinhos[atual] if n not in visitados)
    return componentes