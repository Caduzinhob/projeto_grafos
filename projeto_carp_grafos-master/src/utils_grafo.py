from grafo import Grafo

def ler_arquivo_dat(nome_arquivo):
    grafo = Grafo()
    capacidade = None

    try:
        with open(nome_arquivo, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]

        # Lê a capacidade do arquivo
        for line in lines:
            if line.startswith('Capacity:'):
                try:
                    capacidade = int(line.split(':')[1].strip())
                    break
                except ValueError:
                    raise ValueError(f"Erro ao converter capacidade para número em {nome_arquivo}")

        if capacidade is None:
            raise ValueError(f"Capacidade não encontrada no arquivo {nome_arquivo}")

        # Remove linhas de comentário e vazias para processamento do grafo
        lines = [line for line in lines if line and not line.startswith('#')]
        
        secao_atual = None
        vertices_processados = 0
        arestas_processadas = 0
        arcos_processados = 0

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

            try:
                if secao_atual == 'ReN':
                    no = parts[0][1:]  # remove o 'N'
                    grafo.add_vertice_req(no)
                    vertices_processados += 1

                elif secao_atual == 'ReE':
                    u, v = parts[1], parts[2]
                    custo = int(parts[3])
                    demanda = int(parts[4]) if len(parts) > 4 else 0
                    grafo.add_aresta_req(u, v, [custo, demanda])
                    arestas_processadas += 1

                elif secao_atual == 'EDGE':
                    if len(parts) >= 3:
                        u, v = parts[1], parts[2]
                        custo = int(parts[3])
                        demanda = 0  # Arestas não requeridas não têm demanda
                        grafo.add_aresta(u, v, [custo, demanda])
                        arestas_processadas += 1

                elif secao_atual == 'ReA':
                    u, v = parts[1], parts[2]
                    custo = int(parts[3])
                    demanda = int(parts[4]) if len(parts) > 4 else 0
                    grafo.add_arco_req(u, v, [custo, demanda])
                    arcos_processados += 1

                elif secao_atual == 'ARC':
                    if len(parts) >= 4 and parts[0].startswith('NrA'):
                        u, v = parts[1], parts[2]
                        custo = int(parts[3])
                        demanda = 0  # Arcos não requeridos não têm demanda
                        grafo.add_arco(u, v, [custo, demanda])
                        arcos_processados += 1

            except (IndexError, ValueError) as e:
                raise ValueError(f"Erro ao processar linha '{line}' na seção {secao_atual}: {str(e)}")

        print(f"  Leitura concluída: {vertices_processados} vértices, {arestas_processadas} arestas, {arcos_processados} arcos")
        return grafo, capacidade

    except Exception as e:
        raise Exception(f"Erro ao ler arquivo {nome_arquivo}: {str(e)}") 