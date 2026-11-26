# Documentação do código com Doxygen

O [Doxygen](https://www.doxygen.nl/) lê os comentários do código e gera um site em HTML. O site traz a descrição de cada módulo, classe e função, os diagramas e as páginas deste diretório `docs/`.

## 1. Instalar

| Sistema | Comando / link |
|---|---|
| Raspberry Pi OS / Ubuntu / Debian | `sudo apt install doxygen graphviz` |
| Windows | Instaladores em [doxygen.nl/download](https://www.doxygen.nl/download.html) e [graphviz.org/download](https://graphviz.org/download/). Marque "adicionar ao PATH" no Graphviz. |
| macOS | `brew install doxygen graphviz` |

O Graphviz é opcional e serve só para desenhar os diagramas, incluindo o da máquina de estados. Sem ele, mude `HAVE_DOT = YES` para `NO` no `Doxyfile`.

Use o Doxygen **1.9.1 ou mais novo**, por causa da opção `PYTHON_DOCSTRING`. Confira com `doxygen --version`.

O Raspberry Pi Zero W é lento. É melhor gerar a documentação **no seu computador**.

## 2. Gerar

Na pasta raiz do projeto, onde fica o `Doxyfile`, rode:

```bash
doxygen Doxyfile
```

Depois abra `docs/doxygen/html/index.html` no navegador.

A pasta `docs/doxygen/` está no `.gitignore`, porque é gerada e não vai para o repositório.

## 3. Como comentar o código

As **docstrings** normais do Python são usadas, com os comandos do Doxygen dentro. Isso funciona porque o `Doxyfile` tem `PYTHON_DOCSTRING = NO`.

### Arquivo (no topo de cada `.py`)

```python
"""
@file sensor.py
@brief Leitura do sensor ultrassônico HC-SR04.

Texto mais longo, se quiser. Aceita **Markdown** e tabelas.
"""
```

### Função ou método

```python
def calcular_calibracao(leituras, margem):
    """
    @brief Calcula a distância de fundo e o limite de disparo.
    @param leituras Lista de distâncias (m) medidas com a área vazia.
    @param margem Quanto mais perto que o fundo (m) algo precisa ficar.
    @return Um objeto Calibracao.
    @exception ValueError Se a lista de leituras estiver vazia.
    """
```

### Classe

```python
class Camera:
    """
    @brief Mantém o buffer circular e salva/para vídeos.
    """
```

### Variáveis e constantes

Use um comentário com **dois** `#` na linha de cima:

```python
## GPIO ligado ao pino Trig do HC-SR04.
PINO_TRIG = 23
```

O mesmo vale para atributos dentro do `__init__`:

```python
## Estado atual da máquina.
self.estado = Estado.ESPERANDO
```

### Comandos mais usados

| Comando | Para quê |
|---|---|
| `@file` | Nome do arquivo |
| `@brief` | Resumo de uma linha |
| `@param nome` | Descreve um parâmetro |
| `@return` | Descreve o retorno |
| `@exception Tipo` | Exceção que pode ser lançada |
| `@note` / `@warning` | Caixa de observação / aviso |
| `@todo` | Pendência (aparece numa lista própria) |
| `@see` | "Veja também" |
| `@dot ... @enddot` | Diagrama Graphviz (veja `logica.MaquinaEstados`) |

## 4. Páginas extras

Todo arquivo `.md` dentro de `docs/` vira uma página na documentação. O `README.md` vira a página inicial, configurada em `USE_MDFILE_AS_MAINPAGE`. Imagens colocadas em `docs/img/` ou `assets/` podem ser usadas nessas páginas.
