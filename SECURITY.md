# Segurança

## Versões suportadas

| Versão | Suporte |
|---|---|
| 1.0.x | ✅ |

## Reportando uma vulnerabilidade

**Não abra uma issue pública** para problemas de segurança. Entre em contato diretamente com os autores (veja o README), descrevendo o problema e como reproduzi-lo. A resposta deve vir em até 7 dias.

## Recomendações para quem usa o projeto

- Use uma **senha forte** no Raspberry Pi. Se possível, use autenticação SSH por chave em vez de senha.
- Mantenha o sistema atualizado: `sudo apt update && sudo apt full-upgrade`.
- O servidor `python3 -m http.server`, sugerido no manual para ver os vídeos, **não tem senha**. Use-o só em redes confiáveis e desligue quando terminar.
- **Não exponha o Raspberry Pi diretamente à internet**, por exemplo com redirecionamento de portas no roteador.
- Lembre que os vídeos podem registrar pessoas. Cuide de onde a câmera é instalada e de quem tem acesso aos arquivos.
