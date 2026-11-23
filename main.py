from collections import deque

# Arquivo de persistência e estruturas inicialmente vazias.
ARQUIVO = 'dados_sistema.txt'
leitores = []
reservas = deque()
devolucoes = []
acervo = {}


# Valida a entrada para evitar campos vazios e conflitos com o delimitador do TXT.
def texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor and '|' not in valor and '\n' not in valor:
            return valor
        print('Informe um valor não vazio e sem o caractere |.')


# Lista: cadastro e busca de leitores pelo código.
def localizar_leitor(codigo):
    for leitor in leitores:
        if leitor['codigo'] == codigo:
            return leitor
    return None


def cadastrar_leitor():
    codigo = texto('Código do leitor: ')
    if localizar_leitor(codigo):
        print('Código já cadastrado.')
        return
    nome = texto('Nome: ')
    leitores.append({'codigo': codigo, 'nome': nome})
    print('Leitor cadastrado.')


def listar_leitores():
    if not leitores:
        print('Nenhum leitor cadastrado.')
    for leitor in leitores:
        print(f"{leitor['codigo']} - {leitor['nome']}")


def editar_leitor():
    leitor = localizar_leitor(texto('Código do leitor: '))
    if leitor:
        leitor['nome'] = texto('Novo nome: ')
        print('Leitor atualizado.')
    else:
        print('Leitor não encontrado.')


def excluir_leitor():
    leitor = localizar_leitor(texto('Código do leitor: '))
    if leitor:
        leitores.remove(leitor)
        print('Leitor excluído.')
    else:
        print('Leitor não encontrado.')


# Fila: as reservas entram pelo fim e são atendidas pelo início (FIFO).
def adicionar_reserva():
    codigo = texto('Código da reserva: ')
    if any(r['codigo'] == codigo for r in reservas):
        print('Reserva já existente.')
        return
    livro = texto('Título do livro: ')
    leitor = texto('Nome do leitor: ')
    reservas.append({'codigo': codigo, 'livro': livro, 'leitor': leitor})
    print('Reserva adicionada ao fim da fila.')


def listar_reservas():
    if not reservas:
        print('Fila vazia.')
    for i, r in enumerate(reservas, 1):
        print(f"{i}. {r['codigo']} - {r['livro']} - {r['leitor']}")


def atualizar_reserva():
    codigo = texto('Código da reserva: ')
    for r in reservas:
        if r['codigo'] == codigo:
            r['livro'] = texto('Novo título: ')
            r['leitor'] = texto('Novo nome do leitor: ')
            print('Reserva atualizada sem alterar sua posição na fila.')
            return
    print('Reserva não encontrada.')


def atender_reserva():
    if reservas:
        # Remove a reserva mais antiga da fila.
        r = reservas.popleft()
        print(f"Reserva atendida: {r['codigo']} - {r['livro']}")
    else:
        print('Fila vazia.')


# Pilha: o último livro devolvido é o primeiro a sair (LIFO).
def registrar_devolucao():
    codigo = texto('Código da devolução: ')
    if any(d['codigo'] == codigo for d in devolucoes):
        print('Código já existente.')
        return
    livro = texto('Título do livro: ')
    devolucoes.append({'codigo': codigo, 'livro': livro})
    print('Livro colocado no topo da pilha.')


def listar_devolucoes():
    if not devolucoes:
        print('Pilha vazia.')
    # Exibe os livros do topo até a base, sem modificar a pilha.
    for d in reversed(devolucoes):
        print(f"{d['codigo']} - {d['livro']}")


def atualizar_topo():
    if devolucoes:
        # O índice -1 corresponde ao último elemento da lista, ou seja, ao topo.
        devolucoes[-1]['livro'] = texto('Novo título do livro do topo: ')
        print('Topo atualizado.')
    else:
        print('Pilha vazia.')


def retirar_topo():
    if devolucoes:
        # Remove somente o elemento do topo.
        d = devolucoes.pop()
        print(f"Livro retirado do topo: {d['livro']}")
    else:
        print('Pilha vazia.')


# Árvore: percorre os dicionários aninhados seguindo o caminho informado.
def obter_no(caminho):
    no = acervo
    for parte in caminho:
        if parte not in no:
            return None
        no = no[parte]
    return no


def ler_caminho():
    entrada = texto('Caminho (categorias separadas por /; raiz = .): ')
    if entrada == '.':
        return []
    return [parte.strip() for parte in entrada.split('/') if parte.strip()]


def adicionar_categoria():
    caminho = ler_caminho()
    pai = obter_no(caminho)
    if pai is None:
        print('Caminho não encontrado.')
        return
    nome = texto('Nova categoria: ')
    if '/' in nome:
        print('O nome não pode conter /.')
    elif nome in pai:
        print('Categoria já existe neste nível.')
    else:
        pai[nome] = {}
        print('Categoria adicionada.')


def mostrar_no(no, nivel=0):
    for nome, filhos in no.items():
        print('  ' * nivel + '- ' + nome)
        # A chamada recursiva percorre as subcategorias com maior recuo.
        mostrar_no(filhos, nivel + 1)


def visualizar_acervo():
    if acervo:
        mostrar_no(acervo)
    else:
        print('Acervo vazio.')


def renomear_categoria():
    caminho = ler_caminho()
    if not caminho:
        print('A raiz não pode ser renomeada.')
        return
    pai = obter_no(caminho[:-1])
    if pai is None or caminho[-1] not in pai:
        print('Categoria não encontrada.')
        return
    novo = texto('Novo nome: ')
    if '/' in novo or (novo in pai and novo != caminho[-1]):
        print('Nome inválido ou já existente.')
        return
    # Troca a chave da categoria preservando seu dicionário de subcategorias.
    pai[novo] = pai.pop(caminho[-1])
    print('Categoria renomeada.')


def excluir_categoria():
    caminho = ler_caminho()
    if not caminho:
        print('A raiz não pode ser excluída.')
        return
    pai = obter_no(caminho[:-1])
    if pai is None or caminho[-1] not in pai:
        print('Categoria não encontrada.')
        return
    # Impede a exclusão de uma categoria que ainda possui subcategorias.
    if pai[caminho[-1]]:
        print('A categoria contém subcategorias. Exclua as filhas primeiro.')
        return
    del pai[caminho[-1]]
    print('Categoria excluída.')


# Gera os caminhos completos da árvore para gravar cada categoria no TXT.
def caminhos_arvore(no, prefixo=None):
    if prefixo is None:
        prefixo = []
    for nome, filhos in no.items():
        caminho = prefixo + [nome]
        yield caminho
        yield from caminhos_arvore(filhos, caminho)


# Persistência: grava as quatro estruturas com identificadores e delimitador |.
def salvar_dados():
    try:
        with open(ARQUIVO, 'w', encoding='utf-8') as arquivo:
            for l in leitores:
                arquivo.write(f"LISTA|{l['codigo']}|{l['nome']}\n")
            for r in reservas:
                arquivo.write(f"FILA|{r['codigo']}|{r['livro']}|{r['leitor']}\n")
            for d in devolucoes:
                arquivo.write(f"PILHA|{d['codigo']}|{d['livro']}\n")
            for caminho in caminhos_arvore(acervo):
                arquivo.write('ARVORE|' + '|'.join(caminho) + '\n')
        print(f'Dados salvos em {ARQUIVO}.')
    except OSError as erro:
        print(f'Erro ao salvar: {erro}')


# Reconstrói os registros em estruturas temporárias antes de substituir os dados atuais.
def carregar_dados():
    novos_leitores, novas_reservas, novas_devolucoes, nova_arvore = [], deque(), [], {}
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as arquivo:
            for numero, linha in enumerate(arquivo, 1):
                linha = linha.rstrip('\n\r')
                if not linha:
                    continue
                campos = linha.split('|')
                tipo = campos[0]
                if tipo == 'LISTA' and len(campos) == 3 and all(campos[1:]):
                    if any(l['codigo'] == campos[1] for l in novos_leitores):
                        raise ValueError('Código de leitor duplicado')
                    novos_leitores.append({'codigo': campos[1], 'nome': campos[2]})
                elif tipo == 'FILA' and len(campos) == 4 and all(campos[1:]):
                    if any(r['codigo'] == campos[1] for r in novas_reservas):
                        raise ValueError('Código de reserva duplicado')
                    novas_reservas.append({'codigo': campos[1], 'livro': campos[2], 'leitor': campos[3]})
                elif tipo == 'PILHA' and len(campos) == 3 and all(campos[1:]):
                    if any(d['codigo'] == campos[1] for d in novas_devolucoes):
                        raise ValueError('Código de devolução duplicado')
                    novas_devolucoes.append({'codigo': campos[1], 'livro': campos[2]})
                elif tipo == 'ARVORE' and len(campos) >= 2 and all(campos[1:]):
                    # Cria os níveis da árvore que ainda não existem.
                    no = nova_arvore
                    for parte in campos[1:]:
                        no = no.setdefault(parte, {})
                else:
                    raise ValueError('Formato inválido')
    except (OSError, ValueError, UnicodeError) as erro:
        print(f'Não foi possível carregar os dados: {erro}.')
        return
    # Substitui os dados em memória somente após a leitura completa do arquivo.
    leitores[:] = novos_leitores
    reservas.clear()
    reservas.extend(novas_reservas)
    devolucoes[:] = novas_devolucoes
    acervo.clear()
    acervo.update(nova_arvore)
    print('Dados carregados com sucesso.')


# Menu principal: associa cada opção numérica à função correspondente.
def menu():
    acoes = {
        '1': cadastrar_leitor, '2': listar_leitores,
        '3': editar_leitor, '4': excluir_leitor,
        '5': adicionar_reserva, '6': listar_reservas,
        '7': atualizar_reserva, '8': atender_reserva,
        '9': registrar_devolucao, '10': listar_devolucoes,
        '11': atualizar_topo, '12': retirar_topo,
        '13': adicionar_categoria, '14': visualizar_acervo,
        '15': renomear_categoria, '16': excluir_categoria,
        '17': salvar_dados, '18': carregar_dados,
    }
    while True:
        print('''\n========== SISTEMA DE BIBLIOTECA ==========
1  - Cadastrar leitor        2  - Listar leitores
3  - Editar leitor           4  - Excluir leitor
5  - Adicionar reserva       6  - Listar reservas
7  - Atualizar reserva       8  - Atender reserva
9  - Registrar devolução    10 - Listar devoluções
11 - Atualizar topo         12 - Retirar topo
13 - Adicionar categoria    14 - Visualizar acervo
15 - Renomear categoria     16 - Excluir categoria
17 - Salvar dados           18 - Carregar dados
0  - Sair
==========================================''')
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '0':
            print('Programa encerrado. Use a opção 17 antes de sair para salvar.')
            break
        acao = acoes.get(opcao)
        if acao:
            acao()
        else:
            print('Opção inválida.')


# Inicia o menu quando o arquivo é executado diretamente.
if __name__ == '__main__':
    menu()
