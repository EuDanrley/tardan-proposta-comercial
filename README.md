# Proposta comercial — Comunidade Tardan

O pedido do cliente e as suas condições aprovadas viram uma proposta editável em Word (.docx) e uma mensagem de envio. Preço e prazo nunca são inventados: o que faltar sai destacado como **A CONFIRMAR**.

## Use em 5 minutos

1. **Baixe:** botão verde **Code → Download ZIP**. Extraia a pasta.
2. Abra `instrucoes/instrucao-pronta.md`, copie o texto entre `--- INÍCIO ---` e `--- FIM ---` e cole numa conversa nova do ChatGPT, Claude ou Gemini.
3. No final, cole o pedido do cliente e o que você oferece, com preço e condições **que você já aprovou**. Responda às perguntas da IA (ou diga "pode gerar").
4. Pegue a proposta pronta:
   - **Sem instalar nada:** copie o texto da proposta (bloco B) para `modelos/proposta-modelo.docx`, troque cada A CONFIRMAR e salve.
   - **Com o gerador:** salve o bloco A como `proposta.json` nesta pasta e rode `python scripts/gerar_proposta.py proposta.json`. Sai `proposta.docx` e `proposta-mensagem.txt`.
5. Confira com o `CHECKLIST.md` e envie com a mensagem pronta.

Quer ver antes? Abra `exemplos/saida-esperada.docx` (ou `saida-esperada.md` no navegador).

## O que você precisa

- Uma conta em ChatGPT, Claude ou Gemini. O plano gratuito serve.
- Word, LibreOffice ou Google Docs para abrir e editar o .docx.
- **Só para o gerador (opcional):** Python 3.9 ou mais novo e o pacote python-docx. Testado no Windows com Python 3.11.9 e python-docx 1.2.0.

### Instalar o gerador (uma vez)

No terminal, dentro da pasta do repositório:

```
python -m venv .venv
.venv\Scripts\activate          (no Mac/Linux: source .venv/bin/activate)
python -m pip install -r scripts/requirements.txt
```

Depois, sempre que for gerar: ative o ambiente (segunda linha) e rode `python scripts/gerar_proposta.py proposta.json`.

Opções úteis:
- `-o pasta/nome.docx` escolhe onde salvar.
- `--estrito` faz o gerador acusar erro se ainda houver A CONFIRMAR (para não enviar rascunho por engano).

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `instrucoes/instrucao-pronta.md` | Texto para colar na IA. É a solução. |
| `instrucoes/projeto-ia.md` | Como deixar fixo num Projeto do Claude/ChatGPT, numa Skill ou no Gemini |
| `instrucoes/claude-skill/proposta-comercial/` e `.zip` | Skill do Claude pronta para enviar |
| `modelos/proposta-modelo.docx` | Proposta em Word com todas as seções, para preencher à mão |
| `modelos/proposta-modelo.json` | Formato em branco que o gerador lê |
| `scripts/gerar_proposta.py` | Gerador: JSON → .docx + mensagem |
| `scripts/requirements.txt` | Pacote necessário para o gerador |
| `exemplos/entrada-ficticia-briefing.md` | Pedido de cliente e condições fictícias |
| `exemplos/entrada-ficticia-proposta.json` | O JSON preenchido a partir desse briefing |
| `exemplos/saida-esperada.docx`, `.md` e `-mensagem.txt` | O resultado do gerador com o exemplo |
| `exemplos/teste-ia-2026-11-02.md` | Registro dos testes: o que funcionou e o que foi corrigido |
| `CHECKLIST.md` | Conferência antes de enviar |

## Quer entender ou adaptar?

As aulas do módulo **02 — Proposta comercial** mostram funcionando (aula 1), como deixar com a cara da sua empresa, com sua tabela de preços e seus casos difíceis (aula 2) e como o gerador funciona por dentro, para ajustar o layout ou ligar numa automação (aula 3).

## Limites

- A IA organiza e redige; **quem define preço, prazo e condição é você**. Revise antes de enviar.
- O gerador não calcula total, não aplica desconto e não calcula datas. Ele copia o que está no JSON.
- O layout do .docx é simples (títulos, tabelas, sem logotipo). Para usar sua identidade visual, veja a aula 2.
- Não envia nada ao cliente. Você revisa e envia.
- Proposta não é contrato. Cláusulas jurídicas (multa, rescisão, garantia) devem ser revisadas por quem é responsável por isso na sua empresa.

## Licença

Veja `LICENCA.md`.
