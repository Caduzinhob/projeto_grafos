class Grafo:
    def __init__(self):
        self.vertices = set()
        self.arestas = {}  # {(u,v): [pesos]}
        self.arcos = {}  # {(u,v): [pesos]}
        self.vertices_req = set()  # {v}
        self.arestas_req = {}  # {(u,v): peso}
        self.arcos_req = {}  # {(u,v): peso}

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

    def mostra_arestas(self):
        print("\nTodas as arestas:")
        for (u, v), pesos in self.arestas.items():
            print(f"{u} — {v}: {pesos}")
        print("\nArestas requeridas:")
        for (u, v), peso in self.arestas_req.items():
            print(f"{u} — {v}: {peso}")

    def mostra_arcos(self):
        print("\nTodos os arcos:")
        for (u, v), pesos in self.arcos.items():
            print(f"{u} → {v}: {pesos}")
        print("\nArcos requeridos:")
        for (u, v), peso in self.arcos_req.items():
            print(f"{u} → {v}: {peso}")

    def contar(self):
        print("\nEstatísticas do Grafo:")
        print(f"Total de Vértices: {len(self.vertices)}")
        print(f"Total de Arestas: {len(self.arestas)}")
        print(f"Total de Arcos: {len(self.arcos)}")
        print(f"Vértices Requeridos: {len(self.vertices_req)}")
        print(f"Arestas Requeridas: {len(self.arestas_req)}")
        print(f"Arcos Requeridos: {len(self.arcos_req)}")
        print(f"Densidade: {self.densidade_grafo():.4f}")
        print(f"Grau Mínimo: {self.grau_minimo()}")
        print(f"Grau Máximo: {self.grau_maximo()}")
        print(f"Caminho Médio: {self.caminho_medio():.2f}")
        print(f"Diâmetro: {self.diametro()}")

    def mostra_intermediacao(self):
        _, intermed = self.floyd_warshall_intermediacao()
        print("\nIntermediação:")
        for no, score in sorted(intermed.items()):
            print(f"Nó {no}: {score}")


def ler_arquivo_dat(nome_arquivo):
    grafo = Grafo()

    with open(nome_arquivo, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]

    secao_atual = None

    for line in lines:
        if line.startswith('ReN.'):
            secao_atual = 'ReN'
            continue
        elif line.startswith('ReE.'):
            secao_atual = 'ReE'
            continue
        elif line.startswith('EDGE'):
            secao_atual = 'EDGE'
            continue
        elif line.startswith('ReA.'):
            secao_atual = 'ReA'
            continue
        elif line.startswith('ARC'):
            secao_atual = 'ARC'
            continue

        parts = line.split()
        if not parts:
            continue

        if secao_atual == 'ReN':
            no = parts[0][1:]  # remove o 'N'
            grafo.add_vertice_req(no)

        elif secao_atual == 'ReE':
            u, v = parts[1], parts[2]
            peso = int(parts[3])
            grafo.add_aresta_req(u, v, peso)

        elif secao_atual == 'EDGE':
            if len(parts) >= 3:
                u, v = parts[0], parts[1]
                peso = int(parts[2])
                grafo.add_aresta(u, v, peso)

        elif secao_atual == 'ReA':
            u, v = parts[1], parts[2]
            peso = int(parts[3])
            grafo.add_arco_req(u, v, peso)

        elif secao_atual == 'ARC':
            if len(parts) >= 4 and parts[0].startswith('NrA'):
                u, v = parts[1], parts[2]
                peso = int(parts[3])
                grafo.add_arco(u, v, peso)

    return grafo


if __name__ == "__main__":
    grafo = ler_arquivo_dat('selected_instances/BHW1.dat')
    grafo.contar()
    grafo.mostra_intermediacao()
#grafo.mostra_arestas()
#grafo.mostra_arcos()