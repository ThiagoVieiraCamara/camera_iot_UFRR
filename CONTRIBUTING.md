# Como contribuir

Obrigado pelo interesse em melhorar o projeto!

## Reportando problemas

Abra uma *issue* usando um dos modelos (bug ou sugestão). Para bugs, inclua:

- O que você fez e o que esperava acontecer
- A mensagem de erro completa (`journalctl -u cameratrap -n 50` ajuda)
- Modelo do Raspberry Pi, da câmera e versão do sistema (`cat /etc/os-release`)

## Enviando mudanças

1. Faça um *fork* e crie um branch: `git checkout -b minha-melhoria`
2. Faça as mudanças seguindo o padrão abaixo.
3. Rode os testes: `python3 -m unittest -v`
4. Faça o commit com uma mensagem clara: `git commit -m "Adiciona notificação por Telegram"`
5. Abra um *Pull Request* preenchendo o modelo.

## Padrão de código

- Python 3, seguindo a [PEP 8](https://peps.python.org/pep-0008/).
- Nomes de variáveis, funções e comentários em **português**.
- Todo arquivo, classe e função deve ter docstring no formato do **Doxygen** (`@file`, `@brief`, `@param`, `@return`). Veja [docs/doxygen.md](docs/doxygen.md).
- Valores ajustáveis vão em `src/cameratrap/config.py`, nunca "fixos" no meio do código.
- Código que acessa hardware fica em `sensor.py` ou `camera.py`. A lógica de decisão fica em `logica.py`, para continuar testável sem o Raspberry Pi.
- Lógica nova deve vir acompanhada de testes em `tests/`.
