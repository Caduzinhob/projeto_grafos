from grafo import Grafo

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