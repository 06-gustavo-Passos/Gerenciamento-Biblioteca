# Sistema de Gerenciamento de Biblioteca

**Disciplina:** Teoria das Estruturas de Dados  
**Projeto final:** Tema 5 — Gerenciamento de Biblioteca  
**Aluno:** Gustavo Henrique Silva Passos  
**Matrícula:** 251-002161  
**Linguagem:** Python 3

## 1. Apresentação

Neste projeto, implementei um sistema de gerenciamento de biblioteca em Python, utilizando as quatro estruturas de dados estudadas na disciplina: Lista, Fila, Pilha e Árvore. Organizei o programa em funções e criei um menu numérico para realizar as operações pelo terminal.

O sistema permite cadastrar leitores, controlar reservas de livros, registrar devoluções e organizar categorias do acervo. Também implementei o salvamento e o carregamento dos registros em um único arquivo de texto, para que os dados possam ser recuperados em outra execução.

## 2. Como executar

### Pelo OnlineGDB

Utilizei o **OnlineGDB** para executar e testar o programa, sem precisar instalar um ambiente de desenvolvimento no computador.

1. Acesse https://www.onlinegdb.com/online_python_compiler.
2. Selecione **Python 3**.
3. Abra o arquivo `main.py` deste repositório e copie seu conteúdo para o editor.
4. Clique em **Run**.
5. No console, digite o número da operação desejada e pressione **Enter**.
6. Antes de sair, use a opção **17 — Salvar dados**. Para encerrar, digite **0**.

Para recuperar os registros, utilize **18 — Carregar dados**, desde que o arquivo `dados_sistema.txt` esteja disponível no ambiente. O armazenamento de arquivos no OnlineGDB pode variar entre sessões; por isso, é importante guardar uma cópia quando necessário.

### Pelo terminal do computador

Com Python 3 instalado, abra o terminal na pasta que contém o arquivo **main.py** e digite o comando **python main.py**. Caso o computador utilize o comando **python3**, digite **python3 main.py**. Em seguida, o menu será exibido no terminal.

Não é necessário instalar pacotes adicionais. Utilizei apenas recursos nativos do Python e o módulo `collections`, da biblioteca padrão.

## 3. Funcionalidades do menu

| Opções | Operações |
|---|---|
| 1 a 4 | Cadastrar, listar, editar e excluir leitores |
| 5 a 8 | Adicionar, listar, atualizar e atender reservas |
| 9 a 12 | Registrar, listar, atualizar e retirar livros devolvidos |
| 13 a 16 | Adicionar, visualizar, renomear e excluir categorias |
| 17 | Salvar dados em arquivo TXT |
| 18 | Carregar dados do arquivo TXT |
| 0 | Encerrar o programa |

## 4. Estruturas de dados e justificativas técnicas

### 4.1. Lista — Cadastro de leitores

Para armazenar os leitores, utilizei uma **lista (`list`)**. Cada registro contém um código e um nome, organizados em um dicionário dentro da lista.

Escolhi essa estrutura porque o cadastro precisa aceitar inclusões, consultas, alterações e exclusões, sem exigir uma ordem específica para remover os registros. Utilizei `append()` para adicionar leitores, um laço `for` para localizar e listar registros e `remove()` para excluir um leitor. Como a busca é feita pelo código, percorro a lista até encontrar o cadastro correspondente. No pior caso, essa busca tem complexidade **O(n)**.

### 4.2. Fila — Reservas de livros

Para controlar as reservas, utilizei uma **fila com `deque`**, importada de `collections`. A fila segue a regra **FIFO (First In, First Out)**: a primeira reserva registrada é a primeira a ser atendida.

Escolhi essa estrutura para manter a ordem de chegada dos pedidos. No código, `append()` insere uma nova reserva no final da fila e `popleft()` remove a reserva mais antiga. Essas duas operações são **O(1)** no `deque`. Também permiti atualizar os dados de uma reserva sem alterar sua posição na fila, mantendo a ordem de atendimento.

### 4.3. Pilha — Livros devolvidos

Para registrar os livros devolvidos, utilizei uma **pilha implementada com `list`**. Seu funcionamento segue a regra **LIFO (Last In, First Out)**: o último livro colocado no topo é o primeiro a ser retirado.

Escolhi a pilha porque ela representa o empilhamento de livros aguardando organização. Utilizei `append()` para inserir uma devolução, `pop()` para retirar o livro do topo e o índice `[-1]` para alterar o registro mais recente. Na listagem, utilizei `reversed()` para mostrar os livros do topo até a base. Inserir e remover no final da lista tem custo amortizado **O(1)**.

### 4.4. Árvore — Categorias do acervo

Para organizar o acervo, implementei uma **árvore com dicionários aninhados**. Cada chave representa uma categoria, e o dicionário associado contém suas subcategorias.

Escolhi essa estrutura porque as áreas do conhecimento possuem uma organização hierárquica. Por exemplo, organizei a categoria **tecnologia**, dentro dela a subcategoria **programacao** e, em um terceiro nível, **python**.

Para inserir uma categoria na raiz, informo `.` como caminho. Para criar uma subcategoria, informo o caminho do nível superior, como `tecnologia/programacao`. Implementei funções para navegar pelos níveis, adicionar categorias, exibir a hierarquia, renomear e excluir. Para evitar apagar subcategorias por acidente, o programa não permite excluir uma categoria que ainda tenha elementos abaixo dela.

## 5. Persistência em arquivo texto

Implementei o salvamento no arquivo **`dados_sistema.txt`**, sem utilizar banco de dados, JSON, CSV ou `pickle`.

Cada linha começa com o identificador da estrutura correspondente, seguido dos campos separados pelo caractere **|**. Nos registros de leitores, utilizo o identificador **LISTA**; nas reservas, **FILA**; nas devoluções, **PILHA**; e nas categorias do acervo, **ARVORE**. Para representar os níveis da árvore, registro o caminho completo da categoria na mesma linha, separando os níveis pelo mesmo delimitador.

Na opção **17**, o programa percorre as quatro estruturas e grava os registros no arquivo. Na opção **18**, lê cada linha, identifica a estrutura correspondente e reconstrói os dados em memória. A ordem dos registros é preservada para manter o funcionamento correto da fila e da pilha.

O programa inicia com as estruturas vazias. O carregamento deve ser solicitado pelo menu, e o salvamento também é manual. Por isso, após fazer alterações, é necessário usar novamente a opção 17.

## 6. Testes realizados

Executei o sistema no OnlineGDB e testei as operações do menu com registros de exemplo. Verifiquei o cadastro, a consulta, a edição e a exclusão de leitores; a ordem de atendimento das reservas; a retirada dos livros pelo topo da pilha; e a criação, renomeação e exclusão de categorias da árvore.

Também testei as opções de salvar e carregar dados. Após encerrar e iniciar novamente o programa, carreguei o arquivo TXT e consultei as categorias que haviam sido gravadas.

## 7. Considerações finais

Com este projeto, apliquei cada estrutura de dados a uma necessidade específica da biblioteca. A lista permite manter os cadastros, a fila organiza as reservas por ordem de chegada, a pilha controla a retirada dos livros devolvidos e a árvore representa as categorias do acervo. A divisão em funções facilitou a organização do código, e o arquivo TXT permitiu recuperar os registros entre execuções.
