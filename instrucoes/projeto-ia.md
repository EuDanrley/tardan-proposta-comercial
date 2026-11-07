# Deixe a solução fixa na sua IA (para usar toda semana)

Colar a instrução pronta toda vez funciona. Se você faz propostas com frequência, vale criar um espaço fixo: aí é só abrir e colar o pedido do cliente.

Conferido nas páginas oficiais de ajuda em **02/11/2026**. Os menus mudam com frequência e podem aparecer traduzidos; se algo não bater, siga o nome mais parecido.

## Opção 1 — Projeto no Claude (claude.ai)

Projetos existem em todos os planos, inclusive o gratuito (no gratuito, até 5 projetos).

1. Em claude.ai, abra **Projects** e crie um projeto novo, por exemplo "Propostas comerciais".
2. Nas instruções do projeto, cole o texto da instrução pronta (`instrucao-pronta.md`, de `--- INÍCIO ---` até antes de "MEU BRIEFING").
3. Em conhecimento do projeto, envie `modelos/proposta-modelo.json`, `exemplos/saida-esperada.md` e um documento com **suas condições comerciais aprovadas** (serviços, preços, formas de pagamento, validade). Assim você não precisa repetir isso em cada proposta.
4. Para usar: abra uma conversa dentro do projeto e cole o pedido do cliente.

Fonte: https://support.claude.com/en/articles/9517075-what-are-projects

## Opção 2 — Skill no Claude (usa sozinho quando você pede uma proposta)

Skills estão disponíveis nos planos Free, Pro, Max, Ultra, Team e Enterprise, e exigem a execução de código ligada.

1. Em **Settings > Capabilities**, ligue **Code execution and file creation** (no layout novo: **Create and edit files**). Em Team/Enterprise, quem administra precisa liberar.
2. Use o arquivo `claude-skill/proposta-comercial.zip` deste repositório (ele já tem a pasta da skill na raiz, como o Claude exige).
3. Vá em **Customize > Skills**, clique em **+**, depois **+ Create skill** e **Upload a skill**. Envie o ZIP e deixe a skill ligada.
4. Para usar: em qualquer conversa, cole o pedido do cliente e peça "monte a proposta". Com a execução de código ligada, o Claude pode tentar gerar o .docx com o script que vai dentro da skill; isso depende de o pacote python-docx estar disponível no ambiente dele, o que **não foi testado** pela equipe.

Fontes: https://support.claude.com/en/articles/12512180-using-skills-in-claude e https://support.claude.com/en/articles/12512198-how-to-create-custom-skills

## Opção 3 — Projeto no ChatGPT

Projetos existem para usuários logados, conforme o plano. Limite de arquivos por projeto: Free 5, Go e Plus 25, Pro 40.

1. Na barra lateral, clique em **New project** e dê um nome.
2. Abra as configurações do projeto e cole a instrução pronta como **instruções do projeto** (elas valem só dentro do projeto).
3. Adicione `modelos/proposta-modelo.json`, `exemplos/saida-esperada.md` e o documento com suas condições comerciais aprovadas como arquivos do projeto.
4. Para usar: nova conversa dentro do projeto, cole o pedido do cliente.

Fonte: https://help.openai.com/en/articles/10169521-projects-in-chatgpt

**GPT personalizado:** a ajuda oficial informa que criar e publicar GPTs novos **não está disponível em contas pessoais** (Free, Go, Plus e Pro); só em espaços de trabalho Business, Enterprise e Edu que permitam. Por isso este repositório usa Projeto, não GPT. Fonte: https://help.openai.com/en/articles/8554397-creating-and-editing-gpts

## Opção 4 — Gemini

O Google informa que, **a partir de novembro de 2026, os Gems deixam de existir em contas pessoais** e passam automaticamente para "skills" (habilidades). Contas Workspace têm prazo maior.

- Se a sua conta ainda mostra **Gems**: em gemini.google.com, abra **Gems > Novo Gem**, dê um nome, cole a instrução pronta nas instruções, adicione os arquivos em **Conhecimento** e salve.
- Se já aparece **Skills/Habilidades**: a página oficial informa que dá para importar um arquivo skill.md em **Configurações > Skills > Upload**. Use `claude-skill/proposta-comercial/SKILL.md`. Esse caminho **não foi testado** pela equipe; se não funcionar, cole a instrução pronta numa conversa.
- Se a criação de skills está liberada no plano gratuito: **não confirmado**.

Fontes: https://support.google.com/gemini/answer/15146780 e https://gemini.google/overview/gems/

## Qual escolher?

- Usa Claude: Projeto (mais simples) ou Skill (funciona em qualquer conversa).
- Usa ChatGPT: Projeto.
- Usa Gemini: veja o que a sua conta mostra hoje; na dúvida, cole a instrução pronta.

## Importante para propostas

Se você deixar uma tabela de preços no projeto, **mantenha-a atualizada** e com data. A IA vai usar o que estiver lá. Preço antigo no projeto vira proposta com preço errado.
