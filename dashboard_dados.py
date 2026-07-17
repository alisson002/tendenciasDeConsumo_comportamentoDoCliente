"""Calculos Pandas das 15 perguntas — cada funcao retorna dados prontos para o dashboard."""
import pandas as pd

CSV = "Shopping Trends And Customer Behaviour Dataset.csv"
VAL = "Purchase Amount (USD)"


def carregar():
    df = pd.read_csv(CSV, index_col=0)
    assert df.shape == (3900, 17), f"dataset inesperado: {df.shape}"
    return df


def kpis(df):
    return {
        "receita": int(df[VAL].sum()),
        "transacoes": len(df),
        "ticket": round(df[VAL].mean(), 2),
        "avaliacao": round(df["Review Rating"].mean(), 2),
        "assinantes_n": int((df["Subscription Status"] == "Yes").sum()),
        "desconto_n": int((df["Discount Applied"] == "Yes").sum()),
    }


def categorias(df):
    g = df.groupby("Category")[VAL].agg(receita="sum", ticket="mean", qtd="count")
    g = g.sort_values("receita", ascending=False)
    g["pct"] = g["receita"] / g["receita"].sum() * 100
    return g.round(2).reset_index().to_dict("records")


def top_itens(df):
    g = df.groupby("Item Purchased").agg(
        qtd=("Customer ID", "count"), ticket=(VAL, "mean"), receita=(VAL, "sum"))
    g = g.sort_values(["qtd", "Item Purchased"], ascending=[False, True]).head(10)
    return g.round(2).reset_index().to_dict("records")


def top_estados(df):
    g = df.groupby("Location").agg(
        qtd=("Customer ID", "count"), receita=(VAL, "sum"), ticket=(VAL, "mean"))
    g = g.sort_values("receita", ascending=False).head(10)
    return g.round(2).reset_index().to_dict("records")


def genero(df):
    g = df.groupby("Gender").agg(
        qtd=("Customer ID", "count"), ticket=(VAL, "mean"),
        aval=("Review Rating", "mean"), prev=("Previous Purchases", "mean"))
    return g.round(2).reset_index().to_dict("records")


def idades(df):
    faixa = pd.cut(df["Age"], bins=[17, 25, 35, 45, 55, 70],
                   labels=["18–25", "26–35", "36–45", "46–55", "56–70"])
    g = df.groupby(faixa, observed=False).agg(
        qtd=("Customer ID", "count"), ticket=(VAL, "mean"), total=(VAL, "sum"))
    return g.round(2).reset_index(names="faixa").to_dict("records")


def frequencia(df):
    ordem = ["Weekly", "Bi-Weekly", "Fortnightly", "Monthly",
             "Quarterly", "Every 3 Months", "Annually"]
    g = df.groupby("Frequency of Purchases").agg(
        qtd=("Customer ID", "count"), ticket=(VAL, "mean")).round(2).reindex(ordem)
    return g.reset_index(names="freq").to_dict("records")


def fidelidade(df):
    faixa = pd.cut(df["Previous Purchases"], bins=[0, 10, 20, 30, 40, 50],
                   labels=["1–10", "11–20", "21–30", "31–40", "41–50"])
    g = df.groupby(faixa, observed=False).agg(
        n=("Customer ID", "count"),
        pct=("Subscription Status", lambda x: (x == "Yes").mean() * 100))
    return g.round(2).reset_index(names="faixa").to_dict("records")


def estacoes(df):
    g = df.groupby("Season").agg(
        qtd=("Customer ID", "count"), receita=(VAL, "sum"), ticket=(VAL, "mean"))
    g = g.round(2).sort_values("qtd", ascending=False)
    return g.reset_index().to_dict("records")


def cores_por_estacao(df):
    g = (df.groupby(["Season", "Color"]).size().reset_index(name="qtd")
         .sort_values(["Season", "qtd", "Color"], ascending=[True, False, True])
         .groupby("Season").head(5))
    return {s: sub[["Color", "qtd"]].values.tolist()
            for s, sub in g.groupby("Season")}


def comparativos(df):
    ass = df.groupby("Subscription Status").agg(
        qtd=("Customer ID", "count"), ticket=(VAL, "mean"),
        aval=("Review Rating", "mean"), prev=("Previous Purchases", "mean")).round(2)
    desc = df.groupby("Discount Applied")[VAL].mean().round(2)
    corr = round(df["Review Rating"].corr(df[VAL]), 4)
    return {"assinatura": ass.reset_index().to_dict("records"),
            "desconto": desc.to_dict(), "corr": corr}


def pagamento_frete(df):
    def grupo(col):
        g = df.groupby(col).agg(qtd=("Customer ID", "count"), ticket=(VAL, "mean"),
                                aval=("Review Rating", "mean"))
        g["pct"] = g["qtd"] / len(df) * 100
        g = g.round(2).sort_values("qtd", ascending=False)
        return g.reset_index().to_dict("records")
    return {"pagamento": grupo("Payment Method"), "frete": grupo("Shipping Type")}


def quartis(df):
    seg = pd.qcut(df[VAL], q=4, labels=["Econômico", "Moderado", "Alto", "Premium"])
    g = df.groupby(seg, observed=False).agg(
        vmin=(VAL, "min"), vmax=(VAL, "max"), ticket=(VAL, "mean"),
        idade=("Age", "mean"), masc=("Gender", lambda x: (x == "Male").mean() * 100),
        ass=("Subscription Status", lambda x: (x == "Yes").mean() * 100),
        aval=("Review Rating", "mean"))
    return g.round(2).reset_index(names="nome").to_dict("records")
