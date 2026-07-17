"""Gera dashboard.html: calcula tudo com Pandas e injeta no template HTML/CSS/JS.

Uso: python gerar_dashboard.py
"""
import json

import dashboard_dados as dd

TEMPLATE = "dashboard_template.html"
SAIDA = "dashboard.html"


def fmt_int(n):
    return f"{int(n):,}".replace(",", ".")


def fmt_usd(n):
    return "$" + fmt_int(n)


def fmt_dec(x, prefixo=""):
    return prefixo + f"{float(x):.2f}".replace(".", ",")


def montar_dados(df):
    k = dd.kpis(df)
    return {
        "kpis": k,
        "kpis_fmt": {
            "receita": fmt_usd(k["receita"]), "transacoes": fmt_int(k["transacoes"]),
            "ticket": fmt_dec(k["ticket"], "$"), "avaliacao": fmt_dec(k["avaliacao"]),
            "ass_pct": f"{k['assinantes_n'] / k['transacoes'] * 100:.0f}%",
            "ass_n": fmt_int(k["assinantes_n"]),
            "desc_pct": f"{k['desconto_n'] / k['transacoes'] * 100:.0f}%",
            "desc_n": fmt_int(k["desconto_n"]),
        },
        "categorias": dd.categorias(df), "itens": dd.top_itens(df),
        "estados": dd.top_estados(df), "genero": dd.genero(df),
        "idades": dd.idades(df), "frequencia": dd.frequencia(df),
        "fidelidade": dd.fidelidade(df), "estacoes": dd.estacoes(df),
        "cores": dd.cores_por_estacao(df), "comp": dd.comparativos(df),
        **dd.pagamento_frete(df), "quartis": dd.quartis(df),
    }


def validar(dados):
    assert len(dados["categorias"]) == 4
    assert len(dados["itens"]) == 10 and len(dados["estados"]) == 10
    assert abs(sum(c["pct"] for c in dados["categorias"]) - 100) < 0.1
    assert len(dados["quartis"]) == 4 and len(dados["cores"]) == 4
    assert dados["kpis"]["receita"] == 233081


def gerar():
    df = dd.carregar()
    dados = montar_dados(df)
    validar(dados)
    template = open(TEMPLATE, encoding="utf-8").read()
    html = template.replace("__DATA__", json.dumps(dados, ensure_ascii=False))
    open(SAIDA, "w", encoding="utf-8").write(html)
    print(f"{SAIDA} gerado — {dados['kpis_fmt']['receita']} em "
          f"{dados['kpis_fmt']['transacoes']} transacoes")


if __name__ == "__main__":
    gerar()
