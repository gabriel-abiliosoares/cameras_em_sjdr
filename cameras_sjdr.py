import networkx as nx

# algortimo para encontrar o menor número de câmeras necessárias para cobrir todas as ruas de São José dos Campos, utilizando uma abordagem gulosa.
def cobertura(G):
    nCobertas = {
        tuple(sorted((u, v)))
        for u, v in G.edges()
        }
    cameras = []

    while nCobertas:

        melhorV = None
        melhorC = 0

        for v in G.nodes():

            cobertura = 0

            for u in G.neighbors(v):
                aresta = tuple(sorted((v, u)))

                if aresta in nCobertas:
                    cobertura += 1

            if cobertura > melhorC:
                melhorC = cobertura
                melhorV = v

        cameras.append(melhorV)

        for u in G.neighbors(melhorV):
            aresta = tuple(sorted((melhorV, u)))
            nCobertas.discard(aresta)

    return cameras

# função para saber se todas as ruas estão cobertas
def todasRuas(G, cameras):

    ruas = set()

    for v in cameras:
        for u in G.neighbors(v):
            ruas.add(tuple(sorted((v, u))))

    return len(ruas) == G.number_of_edges()

#verifica se todas as cameras são necessariamente necessárias, ou seja, se é possível retirar alguma câmera sem perder a cobertura de todas as ruas
def retiraRedundantes(G, cameras):

    cameras = cameras.copy()

    mudou = True

    while mudou:

        mudou = False

        for v in cameras.copy():

            teste = cameras.copy()
            teste.remove(v)

            if todasRuas(G, teste):
                cameras.remove(v)
                mudou = True

    return cameras


#imprime o número de câmeras necessárias e as ruas monitoradas por cada câmera.
def mostrarCameras(G, cameras):

    print(f"Número de câmeras necessárias: {len(cameras)}")

    for camera in cameras:

        print(f"\nCâmera na esquina {camera}")

        ruasMonitoradas = set()

        for vizinho in G.neighbors(camera):

            dados = G.get_edge_data(camera, vizinho)

            rua = str(dados.get("name", "Rua sem nome"))

            ruasMonitoradas.add(rua)

        for rua in ruasMonitoradas:
            print(" -", rua)

G = nx.read_gml("sjdr.gml")

cameras = retiraRedundantes(G, cobertura(G))
mostrarCameras(G, cameras)