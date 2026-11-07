"""Gera uma proposta comercial editável (.docx) a partir de um arquivo proposta.json.

Uso:
    python scripts/gerar_proposta.py caminho/proposta.json
    python scripts/gerar_proposta.py caminho/proposta.json -o caminho/saida.docx
    python scripts/gerar_proposta.py caminho/proposta.json --estrito

O script não inventa nada: campo vazio ou ausente vira "A CONFIRMAR".
Todo texto com "A CONFIRMAR" sai destacado em amarelo e entra na lista
"Antes de enviar" no topo do documento. Valores e prazos são copiados como
estão no JSON; o script não calcula preço, total nem data.

Com --estrito, o script termina com código 2 se houver item A CONFIRMAR
(útil para não enviar rascunho por engano).

Comunidade Tardan — uso licenciado a membros (ver LICENCA.md).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.enum.text import WD_COLOR_INDEX
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError:  # pragma: no cover - mensagem para quem não instalou
    sys.exit(
        "Falta o pacote python-docx. Instale com:\n"
        "    python -m pip install -r scripts/requirements.txt\n"
        "(de preferência dentro de um ambiente virtual; veja o README)."
    )

MARCA = "A CONFIRMAR"
pendencias: list[str] = []


# ---------------------------------------------------------------- utilidades

def texto(valor, rotulo: str) -> str:
    """Devolve o texto do campo; vazio vira A CONFIRMAR e é registrado."""
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        valor = MARCA
    valor = str(valor).strip()
    if MARCA.lower() in valor.lower():
        pendencias.append(f"{rotulo}: {valor}")
    return valor


def lista(valor) -> list:
    if valor is None:
        return []
    if isinstance(valor, list):
        return [v for v in valor if not (isinstance(v, str) and not v.strip())]
    return [valor]


def sombrear(celula, cor_hex: str) -> None:
    tc_pr = celula._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), cor_hex)
    tc_pr.append(shd)


def escrever(paragrafo, conteudo: str, negrito: bool = False, tamanho: float | None = None):
    """Escreve o texto destacando cada trecho A CONFIRMAR."""
    partes = []
    resto = conteudo
    while True:
        pos = resto.upper().find(MARCA)
        if pos < 0:
            partes.append((resto, False))
            break
        partes.append((resto[:pos], False))
        partes.append((resto[pos:pos + len(MARCA)], True))
        resto = resto[pos + len(MARCA):]
    for trecho, marcar in partes:
        if not trecho:
            continue
        run = paragrafo.add_run(trecho)
        run.bold = negrito or marcar
        if tamanho:
            run.font.size = Pt(tamanho)
        if marcar:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return paragrafo


def titulo(doc, conteudo: str, nivel: int = 1):
    h = doc.add_heading(level=nivel)
    escrever(h, conteudo)
    return h


def paragrafo(doc, conteudo: str, **kw):
    return escrever(doc.add_paragraph(), conteudo, **kw)


def marcadores(doc, itens: list[str]):
    for item in itens:
        escrever(doc.add_paragraph(style="List Bullet"), item)


def tabela(doc, cabecalho: list[str], linhas: list[list[str]]):
    t = doc.add_table(rows=1, cols=len(cabecalho))
    t.style = "Table Grid"
    for i, nome in enumerate(cabecalho):
        cel = t.rows[0].cells[i]
        cel.text = ""
        escrever(cel.paragraphs[0], nome, negrito=True)
        sombrear(cel, "E7E6E6")
    for linha in linhas:
        cels = t.add_row().cells
        for i, valor in enumerate(linha):
            cels[i].text = ""
            escrever(cels[i].paragraphs[0], valor)
    doc.add_paragraph()
    return t


# ---------------------------------------------------------------- documento

def montar(dados: dict, destino: Path) -> Path:
    fornecedor = dados.get("fornecedor") or {}
    cliente = dados.get("cliente") or {}
    prop = dados.get("proposta") or {}
    inv = dados.get("investimento") or {}

    # Lê e valida tudo antes de escrever, para a lista de pendências ficar completa.
    f_nome = texto(fornecedor.get("nome"), "Nome da sua empresa")
    f_resp = texto(fornecedor.get("responsavel"), "Responsável pela proposta")
    f_contato = texto(fornecedor.get("contato"), "Seu contato")
    f_doc = (fornecedor.get("documento") or "").strip()  # opcional
    c_nome = texto(cliente.get("nome"), "Nome do cliente")
    c_contato = (cliente.get("contato") or "").strip()  # opcional
    p_titulo = texto(prop.get("titulo"), "Título da proposta")
    p_numero = (prop.get("numero") or "").strip()  # opcional
    p_data = texto(prop.get("data"), "Data da proposta")
    p_validade = texto(prop.get("validade"), "Validade da proposta")
    contexto = texto(dados.get("contexto"), "Contexto do pedido")
    objetivo = texto(dados.get("objetivo"), "Objetivo")

    entregaveis = []
    for n, e in enumerate(lista(dados.get("entregaveis")), 1):
        e = e if isinstance(e, dict) else {"item": str(e), "descricao": ""}
        entregaveis.append([
            texto(e.get("item"), f"Entregável {n}"),
            texto(e.get("descricao"), f"Descrição do entregável {n}"),
        ])
    if not entregaveis:
        entregaveis.append([texto(None, "Entregáveis"), ""])

    fora = [texto(x, "Fora do escopo") for x in lista(dados.get("fora_do_escopo"))]
    resp_cli = [texto(x, "Responsabilidade do cliente") for x in lista(dados.get("responsabilidades_cliente"))]
    resp_for = [texto(x, "Responsabilidade da sua empresa") for x in lista(dados.get("responsabilidades_fornecedor"))]

    etapas = []
    for n, e in enumerate(lista(dados.get("etapas")), 1):
        e = e if isinstance(e, dict) else {"etapa": str(e), "prazo": ""}
        etapas.append([
            texto(e.get("etapa"), f"Etapa {n}"),
            texto(e.get("prazo"), f"Prazo da etapa {n}"),
        ])
    if not etapas:
        etapas.append([texto(None, "Etapas e prazos"), MARCA])

    itens_inv = []
    for n, i in enumerate(lista(inv.get("itens")), 1):
        i = i if isinstance(i, dict) else {"descricao": str(i), "valor": ""}
        itens_inv.append([
            texto(i.get("descricao"), f"Item de investimento {n}"),
            texto(i.get("valor"), f"Valor do item {n}"),
        ])
    if not itens_inv:
        itens_inv.append([texto(None, "Itens do investimento"), MARCA])
    total = texto(inv.get("total"), "Valor total")
    pagamento = texto(inv.get("forma_pagamento"), "Forma de pagamento")
    obs_inv = (inv.get("observacoes") or "").strip()
    if obs_inv:
        obs_inv = texto(obs_inv, "Observação do investimento")

    condicoes = [texto(x, "Condição") for x in lista(dados.get("condicoes"))]
    proximo = texto(dados.get("proximo_passo"), "Próximo passo")

    # ---- documento
    doc = Document()
    sec = doc.sections[0]
    for lado in ("left_margin", "right_margin"):
        setattr(sec, lado, Cm(2.2))
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)

    rodape = sec.footer.paragraphs[0]
    rodape.text = f"{f_nome} — Proposta {p_numero}".strip(" —")
    if pendencias:
        rodape.text += " — RASCUNHO: há itens A CONFIRMAR"
    for run in rodape.runs:
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # Quadro "Antes de enviar"
    quadro = doc.add_table(rows=1, cols=1)
    quadro.style = "Table Grid"
    cel = quadro.rows[0].cells[0]
    if pendencias:
        sombrear(cel, "FFF2CC")
        cel.text = ""
        escrever(cel.paragraphs[0], f"ANTES DE ENVIAR — {len(pendencias)} item(ns) A CONFIRMAR", negrito=True)
        for p in pendencias:
            escrever(cel.add_paragraph(), "• " + p, tamanho=9.5)
        escrever(cel.add_paragraph(),
                 "Preencha ou confirme cada item, apague este quadro e gere/salve de novo. "
                 "Não envie ao cliente com itens A CONFIRMAR.", tamanho=9.5)
    else:
        sombrear(cel, "E2EFDA")
        cel.text = ""
        escrever(cel.paragraphs[0],
                 "Nenhum item A CONFIRMAR encontrado. Revise com o CHECKLIST.md e apague este quadro antes de enviar.",
                 negrito=True, tamanho=9.5)
    doc.add_paragraph()

    # Cabeçalho da proposta
    h = doc.add_heading(level=0)
    escrever(h, p_titulo)
    linha_cab = f"Para: {c_nome}"
    if c_contato:
        linha_cab += f" ({c_contato})"
    paragrafo(doc, linha_cab, negrito=True)
    linha_de = f"De: {f_nome} — {f_resp} — {f_contato}"
    if f_doc:
        linha_de += f" — {f_doc}"
    paragrafo(doc, linha_de)
    meta = f"Data: {p_data} · Validade: {p_validade}"
    if p_numero:
        meta = f"Proposta nº {p_numero} · " + meta
    paragrafo(doc, meta)

    titulo(doc, "1. Contexto")
    paragrafo(doc, contexto)
    titulo(doc, "2. Objetivo")
    paragrafo(doc, objetivo)

    titulo(doc, "3. Escopo e entregáveis")
    tabela(doc, ["Entregável", "Descrição"], entregaveis)
    if fora:
        titulo(doc, "Não está incluído nesta proposta", 2)
        marcadores(doc, fora)

    if resp_for or resp_cli:
        titulo(doc, "4. Responsabilidades")
        if resp_for:
            titulo(doc, f"De {f_nome}", 2)
            marcadores(doc, resp_for)
        if resp_cli:
            titulo(doc, f"De {c_nome}", 2)
            marcadores(doc, resp_cli)

    titulo(doc, "5. Etapas e prazos")
    tabela(doc, ["Etapa", "Prazo"], etapas)

    titulo(doc, "6. Investimento")
    tabela(doc, ["Item", "Valor"], itens_inv)
    paragrafo(doc, f"Total: {total}", negrito=True)
    paragrafo(doc, f"Forma de pagamento: {pagamento}")
    if obs_inv:
        paragrafo(doc, obs_inv)

    if condicoes:
        titulo(doc, "7. Condições")
        marcadores(doc, condicoes)

    titulo(doc, "8. Próximo passo")
    paragrafo(doc, proximo)

    doc.add_paragraph()
    paragrafo(doc, f"{f_resp}\n{f_nome}\n{f_contato}")

    destino.parent.mkdir(parents=True, exist_ok=True)
    doc.save(destino)
    return destino


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Gera proposta comercial .docx a partir de proposta.json")
    ap.add_argument("json", help="arquivo proposta.json")
    ap.add_argument("-o", "--saida", help="arquivo .docx de saída (padrão: mesmo nome do JSON)")
    ap.add_argument("--estrito", action="store_true", help="termina com erro (código 2) se houver item A CONFIRMAR")
    args = ap.parse_args(argv)
    try:  # evita erro de acentuação em terminais antigos do Windows
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass

    origem = Path(args.json)
    if not origem.exists():
        print(f"Não encontrei o arquivo: {origem}")
        return 1
    try:
        dados = json.loads(origem.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as erro:
        print(f"O JSON tem um erro na linha {erro.lineno}, coluna {erro.colno}: {erro.msg}")
        print("Dica: peça à IA 'revise e devolva só o JSON válido' e salve de novo.")
        return 1
    if not isinstance(dados, dict):
        print("O JSON precisa ser um objeto { ... } no formato de modelos/proposta-modelo.json.")
        return 1

    destino = Path(args.saida) if args.saida else origem.with_suffix(".docx")
    montar(dados, destino)
    print(f"Proposta gerada: {destino}")

    mensagem = (dados.get("mensagem_envio") or "").strip()
    if mensagem:
        arq_msg = destino.with_name(destino.stem + "-mensagem.txt")
        arq_msg.write_text(mensagem + "\n", encoding="utf-8")
        print(f"Mensagem de envio: {arq_msg}")
        if MARCA.lower() in mensagem.lower():
            pendencias.append("Mensagem de envio: contém A CONFIRMAR")

    if pendencias:
        print(f"\nAtenção: {len(pendencias)} item(ns) {MARCA}:")
        for p in pendencias:
            print("  - " + p)
        print("Esses itens estão destacados em amarelo no documento. Não envie antes de resolver.")
        if args.estrito:
            return 2
    else:
        print("Nenhum item A CONFIRMAR. Revise com o CHECKLIST.md antes de enviar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
