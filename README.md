# Tendencias de Consumo e Comportamento do Cliente

Analise exploratoria de dados de **tendencias de compras e comportamento de clientes**, abrangendo **3.900 transacoes** de um e-commerce com informacoes demograficas, produtos, avaliacoes e habitos de consumo. O projeto responde **15 perguntas analiticas** utilizando **Pandas** e **PostgreSQL**, gerando insights sobre padroes de consumo, preferencias de clientes e oportunidades de negocio.

---

## Sobre os Dados

| Arquivo | Descricao | Registros |
|---------|-----------|-----------|
| `Shopping Trends And Customer Behaviour Dataset.csv` | Dados de compras e comportamento de clientes | 3.900 registros, 17 colunas |

**Fonte:** [Kaggle - Shopping Trends and Customer Behaviour Dataset](https://www.kaggle.com/datasets/sahilislam007/shopping-trends-and-customer-behaviour-dataset)

### Principais Variaveis

| Variavel | Descricao | Tipo | Exemplos |
|----------|-----------|------|----------|
| Customer ID | Identificador unico do cliente | Numerico | 1 a 3.900 |
| Age | Idade do cliente | Numerico | 18 a 70 anos |
| Gender | Genero | Categorico | Male, Female |
| Item Purchased | Produto comprado | Categorico | Blouse, Pants, Jewelry... (25 itens) |
| Category | Categoria do produto | Categorico | Clothing, Accessories, Footwear, Outerwear |
| Purchase Amount (USD) | Valor da compra em dolares | Numerico | $20 a $100 |
| Location | Estado (EUA) | Categorico | 50 estados americanos |
| Color | Cor do produto | Categorico | 25 cores diferentes |
| Season | Estacao do ano | Categorico | Spring, Summer, Fall, Winter |
| Review Rating | Avaliacao do produto | Numerico | 2.5 a 5.0 |
| Subscription Status | Cliente possui assinatura? | Categorico | Yes, No |
| Shipping Type | Tipo de frete | Categorico | Free Shipping, Express, Standard... |
| Discount Applied | Desconto aplicado? | Categorico | Yes, No |
| Promo Code Used | Codigo promocional usado? | Categorico | Yes, No |
| Previous Purchases | Quantidade de compras anteriores | Numerico | 1 a 50 |
| Payment Method | Metodo de pagamento | Categorico | Credit Card, PayPal, Cash... (6 metodos) |
| Frequency of Purchases | Frequencia de compras | Categorico | Weekly, Monthly, Annually... (7 niveis) |

---

## 15 Perguntas e Respostas

Cada pergunta e respondida com duas abordagens: **Pandas** (Python) e **PostgreSQL**.

---

### Pergunta 1: Quais sao as categorias de produtos com maior receita total e qual a participacao percentual de cada uma?

**Objetivo:** Entender a distribuicao de receita entre as categorias e identificar quais segmentos impulsionam o faturamento.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> receita_categoria = (
>     df.groupby('Category')['Purchase Amount (USD)']
>     .agg(Receita_Total='sum', Ticket_Medio='mean', Qtd_Compras='count')
>     .sort_values('Receita_Total', ascending=False)
> )
> receita_categoria['Participacao_%'] = (
>     receita_categoria['Receita_Total'] / receita_categoria['Receita_Total'].sum() * 100
> ).round(2)
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Category",
>        SUM("Purchase Amount (USD)") AS receita_total,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        COUNT(*) AS qtd_compras,
>        ROUND(SUM("Purchase Amount (USD)") * 100.0 /
>              (SELECT SUM("Purchase Amount (USD)") FROM shopping_trends), 2) AS participacao_pct
> FROM shopping_trends
> GROUP BY "Category"
> ORDER BY receita_total DESC;
> ```

</details>

**Insight:** **Clothing** domina com **44,73%** da receita total ($104.264), seguido por **Accessories** (31,83%), **Footwear** (15,49%) e **Outerwear** (7,95%). Apesar da diferenca de volume, o ticket medio e muito similar entre categorias (~$57-60), indicando que a lideranca de Clothing vem do **volume de vendas** (1.737 transacoes) e nao de precos mais altos.

---

### Pergunta 2: Como o comportamento de compra difere entre homens e mulheres?

**Objetivo:** Identificar diferencas de consumo entre generos para direcionar estrategias de marketing.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> genero = (
>     df.groupby('Gender').agg(
>         qtd_compras=('Customer ID', 'count'),
>         ticket_medio=('Purchase Amount (USD)', 'mean'),
>         avaliacao_media=('Review Rating', 'mean'),
>         compras_anteriores=('Previous Purchases', 'mean')
>     ).round(2)
> )
>
> # Distribuicao por categoria e genero
> cat_genero = df.groupby(['Gender', 'Category']).size().unstack(fill_value=0)
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Gender",
>        COUNT(*) AS qtd_compras,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        ROUND(AVG("Review Rating")::numeric, 2) AS avaliacao_media,
>        ROUND(AVG("Previous Purchases")::numeric, 2) AS compras_anteriores
> FROM shopping_trends
> GROUP BY "Gender";
>
> -- Distribuicao por categoria e genero
> SELECT "Gender", "Category", COUNT(*) AS qtd
> FROM shopping_trends
> GROUP BY "Gender", "Category"
> ORDER BY "Gender", qtd DESC;
> ```

</details>

**Insight:** O publico masculino representa **68%** das compras (2.652), porem o ticket medio e praticamente identico entre generos ($59,54 para homens vs. $60,25 para mulheres). As avaliacoes e o historico de compras anteriores tambem sao muito semelhantes, sugerindo que **a diferenca esta no volume de clientes e nao no comportamento individual**. A proporcao entre categorias se mantem consistente em ambos os generos.

---

### Pergunta 3: Como o valor de compra varia entre diferentes faixas etarias?

**Objetivo:** Segmentar clientes por idade para identificar os grupos que mais consomem e direcionar acoes comerciais.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> bins = [17, 25, 35, 45, 55, 70]
> labels = ['18-25', '26-35', '36-45', '46-55', '56-70']
> df['Faixa_Etaria'] = pd.cut(df['Age'], bins=bins, labels=labels)
>
> faixa_etaria = (
>     df.groupby('Faixa_Etaria', observed=False).agg(
>         qtd_compras=('Customer ID', 'count'),
>         ticket_medio=('Purchase Amount (USD)', 'mean'),
>         valor_total=('Purchase Amount (USD)', 'sum'),
>         avaliacao_media=('Review Rating', 'mean')
>     ).round(2)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT CASE
>          WHEN "Age" BETWEEN 18 AND 25 THEN '18-25'
>          WHEN "Age" BETWEEN 26 AND 35 THEN '26-35'
>          WHEN "Age" BETWEEN 36 AND 45 THEN '36-45'
>          WHEN "Age" BETWEEN 46 AND 55 THEN '46-55'
>          ELSE '56-70'
>        END AS faixa_etaria,
>        COUNT(*) AS qtd_compras,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        SUM("Purchase Amount (USD)") AS valor_total,
>        ROUND(AVG("Review Rating")::numeric, 2) AS avaliacao_media
> FROM shopping_trends
> GROUP BY faixa_etaria
> ORDER BY faixa_etaria;
> ```

</details>

**Insight:** A faixa **56-70 anos** lidera em volume com **1.105 compras** (28,3% do total) e receita total de $65.256, demonstrando que clientes mais velhos sao os mais ativos na plataforma. O ticket medio, porem, e notavelmente **uniforme** entre todas as faixas ($59-61), indicando que a idade influencia a **frequencia de compra**, mas nao o **valor gasto por transacao**.

---

### Pergunta 4: Quais sao os 10 itens mais vendidos e qual o ticket medio de cada um?

**Objetivo:** Identificar os produtos mais populares e entender a faixa de preco de cada um.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> top_itens = (
>     df.groupby('Item Purchased').agg(
>         qtd_vendas=('Customer ID', 'count'),
>         ticket_medio=('Purchase Amount (USD)', 'mean'),
>         receita_total=('Purchase Amount (USD)', 'sum')
>     )
>     .sort_values('qtd_vendas', ascending=False)
>     .head(10)
>     .round(2)
> )
> top_itens.index.name = 'Item'
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Item Purchased",
>        COUNT(*) AS qtd_vendas,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        SUM("Purchase Amount (USD)") AS receita_total
> FROM shopping_trends
> GROUP BY "Item Purchased"
> ORDER BY qtd_vendas DESC
> LIMIT 10;
> ```

</details>

**Insight:** **Blouse** e **Pants** lideram com **171 vendas** cada, seguidos por **Jewelry** (171). A distribuicao e extremamente equilibrada entre os 25 itens (variando de 140 a 171 vendas), sugerindo uma base de clientes com **demanda diversificada**. O ticket medio varia pouco ($56-62), com **Dress** apresentando o maior valor ($62,17) e **Jacket** o menor ($56,74).

---

### Pergunta 5: Como as vendas se distribuem entre as estacoes do ano? Existe sazonalidade nas categorias?

**Objetivo:** Detectar padroes sazonais que possam orientar planejamento de estoque e campanhas.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> sazonalidade = (
>     df.groupby('Season').agg(
>         qtd_compras=('Customer ID', 'count'),
>         receita_total=('Purchase Amount (USD)', 'sum'),
>         ticket_medio=('Purchase Amount (USD)', 'mean')
>     ).round(2)
> )
>
> # Quantidade de vendas por categoria em cada estacao
> cat_sazonal = (
>     df.groupby(['Season', 'Category'])
>     .size()
>     .unstack(fill_value=0)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Season",
>        COUNT(*) AS qtd_compras,
>        SUM("Purchase Amount (USD)") AS receita_total,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio
> FROM shopping_trends
> GROUP BY "Season"
> ORDER BY qtd_compras DESC;
>
> -- Categorias por estacao
> SELECT "Season", "Category", COUNT(*) AS qtd_compras
> FROM shopping_trends
> GROUP BY "Season", "Category"
> ORDER BY "Season", qtd_compras DESC;
> ```

</details>

**Insight:** **Spring** lidera em volume (999 compras), mas **Fall** tem o maior ticket medio ($61,56) e a maior receita ($60.018). As categorias mantem proporcoes semelhantes em todas as estacoes, indicando que **nao ha sazonalidade marcante** por categoria. A distribuicao equilibrada sugere um consumo estavel ao longo do ano, sem picos tipicos de datas comemorativas.

---

### Pergunta 6: Clientes com assinatura gastam mais e avaliam melhor os produtos?

**Objetivo:** Avaliar se o modelo de assinatura gera maior engajamento e receita.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> assinatura = (
>     df.groupby('Subscription Status').agg(
>         qtd_clientes=('Customer ID', 'count'),
>         ticket_medio=('Purchase Amount (USD)', 'mean'),
>         avaliacao_media=('Review Rating', 'mean'),
>         compras_anteriores=('Previous Purchases', 'mean')
>     ).round(2)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Subscription Status",
>        COUNT(*) AS qtd_clientes,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        ROUND(AVG("Review Rating")::numeric, 2) AS avaliacao_media,
>        ROUND(AVG("Previous Purchases")::numeric, 2) AS compras_anteriores
> FROM shopping_trends
> GROUP BY "Subscription Status";
> ```

</details>

**Insight:** Apenas **27%** dos clientes possuem assinatura (1.053 de 3.900). Surpreendentemente, **nao ha diferenca significativa** entre assinantes e nao-assinantes: ticket medio ($59,49 vs. $59,87), avaliacao (3,74 vs. 3,75) e compras anteriores (26,08 vs. 25,08) sao praticamente identicos. Isso sugere que o programa de assinatura **nao esta gerando valor diferenciado**, representando uma oportunidade de melhoria na proposta de valor para assinantes.

---

### Pergunta 7: Qual o impacto de descontos e codigos promocionais no valor de compra?

**Objetivo:** Medir a efetividade das estrategias de desconto e promocao.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> desconto_promo = (
>     df.groupby(['Discount Applied', 'Promo Code Used']).agg(
>         qtd_compras=('Customer ID', 'count'),
>         ticket_medio=('Purchase Amount (USD)', 'mean'),
>         avaliacao_media=('Review Rating', 'mean')
>     ).round(2)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Discount Applied", "Promo Code Used",
>        COUNT(*) AS qtd_compras,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        ROUND(AVG("Review Rating")::numeric, 2) AS avaliacao_media
> FROM shopping_trends
> GROUP BY "Discount Applied", "Promo Code Used"
> ORDER BY ticket_medio DESC;
> ```

</details>

**Insight:** Desconto e codigo promocional **sempre ocorrem juntos** — todas as 1.677 compras com desconto tambem usaram promo code, e vice-versa. O impacto no valor e minimo: compras sem desconto tem ticket medio de **$60,13** vs. **$59,28** com desconto, uma diferenca de apenas $0,85. Isso indica que os descontos oferecidos sao pequenos ou que o valor registrado ja e o valor liquido. A taxa de uso de promocoes e de **43%**, mostrando boa adesao.

---

### Pergunta 8: Quais metodos de pagamento sao mais utilizados e qual o ticket medio associado?

**Objetivo:** Mapear preferencias de pagamento para otimizar gateways e experiencia de checkout.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> pagamento = (
>     df.groupby('Payment Method').agg(
>         qtd_compras=('Customer ID', 'count'),
>         ticket_medio=('Purchase Amount (USD)', 'mean'),
>         receita_total=('Purchase Amount (USD)', 'sum')
>     )
>     .sort_values('qtd_compras', ascending=False)
>     .round(2)
> )
> pagamento['Participacao_%'] = (
>     pagamento['qtd_compras'] / pagamento['qtd_compras'].sum() * 100
> ).round(2)
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Payment Method",
>        COUNT(*) AS qtd_compras,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        SUM("Purchase Amount (USD)") AS receita_total,
>        ROUND(COUNT(*) * 100.0 /
>              (SELECT COUNT(*) FROM shopping_trends), 2) AS participacao_pct
> FROM shopping_trends
> GROUP BY "Payment Method"
> ORDER BY qtd_compras DESC;
> ```

</details>

**Insight:** Os metodos de pagamento sao distribuidos de forma **extremamente equilibrada**, variando de 15,69% (Bank Transfer) a 17,36% (PayPal). **Debit Card** tem o maior ticket medio ($60,92), enquanto **Venmo** tem o menor ($58,95). A diversificacao indica que os clientes nao tem forte preferencia por um metodo especifico, reforcando a importancia de **manter todos os gateways ativos**.

---

### Pergunta 9: Existe correlacao entre a avaliacao do produto e o valor gasto na compra?

**Objetivo:** Investigar se clientes que pagam mais avaliam melhor os produtos.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> correlacao = df['Review Rating'].corr(df['Purchase Amount (USD)'])
> print(f'Correlacao de Pearson: {correlacao:.4f}')
>
> # Media de gasto por faixa de avaliacao
> df['Faixa_Avaliacao'] = pd.cut(
>     df['Review Rating'],
>     bins=[2.4, 3.0, 3.5, 4.0, 4.5, 5.01],
>     labels=['2.5-3.0', '3.1-3.5', '3.6-4.0', '4.1-4.5', '4.6-5.0']
> )
> avaliacao_valor = (
>     df.groupby('Faixa_Avaliacao', observed=False).agg(
>         qtd_compras=('Customer ID', 'count'),
>         ticket_medio=('Purchase Amount (USD)', 'mean')
>     ).round(2)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> -- Correlacao de Pearson
> SELECT ROUND(CORR("Review Rating", "Purchase Amount (USD)")::numeric, 4) AS correlacao
> FROM shopping_trends;
>
> -- Media por faixa de avaliacao
> SELECT CASE
>          WHEN "Review Rating" <= 3.0 THEN '2.5-3.0'
>          WHEN "Review Rating" <= 3.5 THEN '3.1-3.5'
>          WHEN "Review Rating" <= 4.0 THEN '3.6-4.0'
>          WHEN "Review Rating" <= 4.5 THEN '4.1-4.5'
>          ELSE '4.6-5.0'
>        END AS faixa_avaliacao,
>        COUNT(*) AS qtd_compras,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio
> FROM shopping_trends
> GROUP BY faixa_avaliacao
> ORDER BY faixa_avaliacao;
> ```

</details>

**Insight:** A correlacao de Pearson e **0,0308** — praticamente **nula**. O ticket medio por faixa de avaliacao varia apenas de $58,94 (notas 2.5-3.0) a $61,00 (notas 4.6-5.0), uma diferenca de apenas $2. Isso demonstra que o valor pago **nao influencia a satisfacao do cliente**, e que a percepcao de qualidade e independente do preco. Fatores como experiencia de compra e qualidade do produto provavelmente pesam mais nas avaliacoes.

---

### Pergunta 10: Quais sao os 10 estados com maior receita e qual o ticket medio por estado?

**Objetivo:** Identificar os mercados geograficos mais relevantes para o negocio.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> top_estados = (
>     df.groupby('Location').agg(
>         qtd_compras=('Customer ID', 'count'),
>         receita_total=('Purchase Amount (USD)', 'sum'),
>         ticket_medio=('Purchase Amount (USD)', 'mean')
>     )
>     .sort_values('receita_total', ascending=False)
>     .head(10)
>     .round(2)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Location",
>        COUNT(*) AS qtd_compras,
>        SUM("Purchase Amount (USD)") AS receita_total,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio
> FROM shopping_trends
> GROUP BY "Location"
> ORDER BY receita_total DESC
> LIMIT 10;
> ```

</details>

**Insight:** **Montana** lidera com **96 compras** e $5.784 em receita, seguido por **Illinois** ($5.617) e **California** ($5.605). Destaque para **West Virginia** que, apesar de ter menos compras (81), possui o maior ticket medio entre o top 10 ($63,88), e **Nevada** com $63,38. A receita e distribuida entre todos os 50 estados de forma relativamente uniforme, sem concentracao excessiva em grandes centros urbanos.

---

### Pergunta 11: Clientes com maior frequencia de compras gastam mais por transacao?

**Objetivo:** Entender se compradores mais frequentes sao tambem os que mais gastam por compra.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> ordem = ['Weekly', 'Bi-Weekly', 'Fortnightly', 'Monthly',
>          'Quarterly', 'Every 3 Months', 'Annually']
>
> frequencia = (
>     df.groupby('Frequency of Purchases').agg(
>         qtd_clientes=('Customer ID', 'count'),
>         ticket_medio=('Purchase Amount (USD)', 'mean'),
>         avaliacao_media=('Review Rating', 'mean'),
>         compras_anteriores=('Previous Purchases', 'mean')
>     ).round(2)
>     .reindex(ordem)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Frequency of Purchases",
>        COUNT(*) AS qtd_clientes,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        ROUND(AVG("Review Rating")::numeric, 2) AS avaliacao_media,
>        ROUND(AVG("Previous Purchases")::numeric, 2) AS compras_anteriores
> FROM shopping_trends
> GROUP BY "Frequency of Purchases"
> ORDER BY CASE "Frequency of Purchases"
>     WHEN 'Weekly' THEN 1
>     WHEN 'Bi-Weekly' THEN 2
>     WHEN 'Fortnightly' THEN 3
>     WHEN 'Monthly' THEN 4
>     WHEN 'Quarterly' THEN 5
>     WHEN 'Every 3 Months' THEN 6
>     WHEN 'Annually' THEN 7
> END;
> ```

</details>

**Insight:** **Nao ha relacao clara** entre frequencia de compras e valor gasto. O ticket medio varia apenas entre $58,97 (Weekly) e $60,69 (Bi-Weekly). Nota-se que **Bi-Weekly** e **Fortnightly** representam a mesma frequencia (quinzenal), assim como **Quarterly** e **Every 3 Months** (trimestral) — uma inconsistencia nos dados que vale monitorar. Os grupos estao distribuidos de forma equilibrada (~539-584 clientes cada).

---

### Pergunta 12: Qual tipo de frete e mais escolhido e como se relaciona com o valor da compra?

**Objetivo:** Analisar preferencias de entrega e seu impacto na experiencia e no ticket medio.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> frete = (
>     df.groupby('Shipping Type').agg(
>         qtd_compras=('Customer ID', 'count'),
>         ticket_medio=('Purchase Amount (USD)', 'mean'),
>         avaliacao_media=('Review Rating', 'mean')
>     )
>     .sort_values('qtd_compras', ascending=False)
>     .round(2)
> )
> frete['Participacao_%'] = (
>     frete['qtd_compras'] / frete['qtd_compras'].sum() * 100
> ).round(2)
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT "Shipping Type",
>        COUNT(*) AS qtd_compras,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        ROUND(AVG("Review Rating")::numeric, 2) AS avaliacao_media,
>        ROUND(COUNT(*) * 100.0 /
>              (SELECT COUNT(*) FROM shopping_trends), 2) AS participacao_pct
> FROM shopping_trends
> GROUP BY "Shipping Type"
> ORDER BY qtd_compras DESC;
> ```

</details>

**Insight:** **Free Shipping** lidera com **17,31%** (675 compras), seguido por **Standard** (16,77%) e **Store Pickup** (16,67%). A distribuicao e muito equilibrada entre os 6 tipos de frete. O **2-Day Shipping** tem o maior ticket medio ($60,73), enquanto **Standard** tem o menor ($58,46). Curiosamente, **Standard** tem a melhor avaliacao media (3,82), sugerindo que expectativas alinhadas com a entrega podem contribuir mais para a satisfacao do que a velocidade.

---

### Pergunta 13: Quais sao as cores mais populares em cada estacao do ano?

**Objetivo:** Identificar tendencias de preferencia cromatica sazonal para orientar colecoes e estoque.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> cores_estacao = (
>     df.groupby(['Season', 'Color'])
>     .size()
>     .reset_index(name='Qtd')
>     .sort_values(['Season', 'Qtd'], ascending=[True, False])
>     .groupby('Season')
>     .head(5)
>     .reset_index(drop=True)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> WITH ranked AS (
>     SELECT "Season", "Color", COUNT(*) AS qtd,
>            ROW_NUMBER() OVER (
>                PARTITION BY "Season" ORDER BY COUNT(*) DESC
>            ) AS rank
>     FROM shopping_trends
>     GROUP BY "Season", "Color"
> )
> SELECT "Season", "Color", qtd
> FROM ranked
> WHERE rank <= 5
> ORDER BY "Season", qtd DESC;
> ```

</details>

**Insight:** Cada estacao possui preferencias cromaticas distintas: **Fall** prefere **Magenta** e **Yellow** (50 cada), **Spring** prefere **Olive** (52), **Summer** destaca **Silver** (59 vendas — o maior valor individual) e **Winter** favorece **Green** (50). A cor **Olive** aparece no top em mais de uma estacao, sendo uma escolha versatil. Esses padroes podem guiar a curadoria de cores por colecao sazonal.

---

### Pergunta 14: Clientes com mais compras anteriores sao mais propensos a ter assinatura?

**Objetivo:** Investigar se a fidelidade (compras acumuladas) se traduz em adesao ao programa de assinatura.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> df['Faixa_Compras'] = pd.cut(
>     df['Previous Purchases'],
>     bins=[0, 10, 20, 30, 40, 50],
>     labels=['1-10', '11-20', '21-30', '31-40', '41-50']
> )
>
> fidelidade = (
>     df.groupby('Faixa_Compras', observed=False).agg(
>         total_clientes=('Customer ID', 'count'),
>         pct_assinantes=('Subscription Status',
>                         lambda x: (x == 'Yes').mean() * 100),
>         ticket_medio=('Purchase Amount (USD)', 'mean')
>     ).round(2)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> SELECT CASE
>          WHEN "Previous Purchases" BETWEEN 1 AND 10 THEN '1-10'
>          WHEN "Previous Purchases" BETWEEN 11 AND 20 THEN '11-20'
>          WHEN "Previous Purchases" BETWEEN 21 AND 30 THEN '21-30'
>          WHEN "Previous Purchases" BETWEEN 31 AND 40 THEN '31-40'
>          ELSE '41-50'
>        END AS faixa_compras,
>        COUNT(*) AS total_clientes,
>        ROUND(AVG(CASE WHEN "Subscription Status" = 'Yes'
>                       THEN 1 ELSE 0 END) * 100, 2) AS pct_assinantes,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio
> FROM shopping_trends
> GROUP BY faixa_compras
> ORDER BY faixa_compras;
> ```

</details>

**Insight:** Existe uma **leve tendencia crescente**: clientes com 1-10 compras tem **23,47%** de taxa de assinatura, subindo para **29,46%** na faixa 31-40. Porem, o grupo 41-50 cai para 27,06%, quebrando o padrao. A correlacao e fraca, sugerindo que o historico de compras sozinho **nao e um forte preditor** de adesao a assinatura. Estrategias ativas de conversao seriam mais eficazes do que esperar a adesao organica.

---

### Pergunta 15: Qual o perfil do cliente que mais gasta? (Segmentacao por quartis de gasto)

**Objetivo:** Criar segmentos de clientes por nivel de gasto e tracar o perfil de cada grupo, identificando oportunidades de upselling.

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> df['Segmento_Gasto'] = pd.qcut(
>     df['Purchase Amount (USD)'],
>     q=4,
>     labels=['Economico', 'Moderado', 'Alto', 'Premium']
> )
>
> perfil = (
>     df.groupby('Segmento_Gasto', observed=False).agg(
>         faixa_valor=('Purchase Amount (USD)',
>                      lambda x: f'${x.min():.0f} - ${x.max():.0f}'),
>         ticket_medio=('Purchase Amount (USD)', 'mean'),
>         idade_media=('Age', 'mean'),
>         pct_masculino=('Gender',
>                        lambda x: (x == 'Male').mean() * 100),
>         pct_assinante=('Subscription Status',
>                        lambda x: (x == 'Yes').mean() * 100),
>         pct_desconto=('Discount Applied',
>                       lambda x: (x == 'Yes').mean() * 100),
>         avaliacao_media=('Review Rating', 'mean'),
>         compras_anteriores=('Previous Purchases', 'mean'),
>         categoria_top=('Category', lambda x: x.mode()[0])
>     ).round(2)
> )
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> WITH quartis AS (
>     SELECT *,
>            NTILE(4) OVER (ORDER BY "Purchase Amount (USD)") AS quartil
>     FROM shopping_trends
> )
> SELECT CASE quartil
>          WHEN 1 THEN 'Economico'
>          WHEN 2 THEN 'Moderado'
>          WHEN 3 THEN 'Alto'
>          WHEN 4 THEN 'Premium'
>        END AS segmento,
>        MIN("Purchase Amount (USD)") || ' - ' ||
>        MAX("Purchase Amount (USD)") AS faixa_valor,
>        ROUND(AVG("Purchase Amount (USD)")::numeric, 2) AS ticket_medio,
>        ROUND(AVG("Age")::numeric, 1) AS idade_media,
>        ROUND(AVG(CASE WHEN "Gender" = 'Male'
>                       THEN 1 ELSE 0 END) * 100, 2) AS pct_masculino,
>        ROUND(AVG(CASE WHEN "Subscription Status" = 'Yes'
>                       THEN 1 ELSE 0 END) * 100, 2) AS pct_assinante,
>        ROUND(AVG(CASE WHEN "Discount Applied" = 'Yes'
>                       THEN 1 ELSE 0 END) * 100, 2) AS pct_desconto,
>        ROUND(AVG("Review Rating")::numeric, 2) AS avaliacao_media,
>        ROUND(AVG("Previous Purchases")::numeric, 1) AS compras_anteriores
> FROM quartis
> GROUP BY quartil
> ORDER BY quartil;
> ```

</details>

**Insight:** A segmentacao revela que os quatro quartis tem perfis **notavelmente similares**: idade media (~44 anos), proporcao masculina (~67-70%), taxa de assinatura (~27%), e avaliacao (~3,7). A unica diferenca real e o valor gasto em si (de $29,52 no Economico a $91,09 no Premium). **Clothing** e a categoria favorita em todos os segmentos. Essa homogeneidade sugere que o valor de compra e influenciado mais pelo **produto escolhido** do que pelo perfil demografico do cliente.

---

## Conclusao

Esta analise explorou 15 dimensoes dos dados de comportamento de compra de clientes, revelando padroes importantes:

| Tema | Perguntas | Principal Descoberta |
|------|-----------|---------------------|
| Receita e Produtos | 1, 4 | Clothing domina em volume; itens muito equilibrados |
| Demografia | 2, 3 | Genero e idade nao impactam valor de compra |
| Sazonalidade | 5, 13 | Distribuicao uniforme; preferencias de cor variam |
| Fidelidade e Assinatura | 6, 14 | Assinatura nao gera diferencial mensuravel |
| Promocoes e Descontos | 7 | Impacto minimo no valor de compra |
| Pagamento e Frete | 8, 12 | Distribuicao equilibrada entre opcoes |
| Correlacoes | 9, 11 | Avaliacao e frequencia independentes do valor |
| Segmentacao | 15 | Perfis muito homogeneos entre segmentos de gasto |
| Geografia | 10 | Receita pulverizada entre estados |

> **Insight geral:** O dataset apresenta distribuicoes surpreendentemente uniformes em quase todas as dimensoes, sugerindo que as variaveis demograficas e comportamentais analisadas **nao sao fortes preditoras** do valor de compra. Isso aponta para a necessidade de coletar dados adicionais (historico de navegacao, tempo no site, campanhas vistas) para modelagens preditivas mais eficazes.

---

## Coleta de Dados (Kaggle API)

O notebook **`analise_tendencias.ipynb`** contem um bloco opcional que acessa os dados diretamente pela **API do Kaggle**, sem necessidade de download manual. Os dados sao baixados para um diretorio temporario (`/tmp/shopping_trends`) e carregados em memoria com Pandas — nenhum arquivo permanece salvo em disco.

Para utilizar, crie e configure sua chave de API no arquivo `.env`:

```
KAGGLE_API_TOKEN=seu_token_aqui
```

> O `.env` deve ser incluido no `.gitignore` para **nao ser enviado ao GitHub**, protegendo suas credenciais.

Se preferir, o arquivo CSV tambem esta disponivel diretamente no repositorio para carregamento local.

---

## Estrutura do Projeto

```
tendenciasDeConsumo_comportamentoDoCliente/
  README.md                                              # Este arquivo
  analise_tendencias.ipynb                               # Notebook com todas as analises
  Shopping Trends And Customer Behaviour Dataset.csv     # Dados de compras
  prompt_contexto_analise_dados.md                       # Prompt para replicar em novos datasets
  .env                                                   # Chaves de API (nao versionado)
  .gitignore                                             # Arquivos ignorados pelo Git
```

## Tecnologias Utilizadas

- **Python 3** (Pandas, NumPy, python-dotenv)
- **PostgreSQL** (queries equivalentes)
- **Jupyter Notebook**
- **Kaggle API** (coleta de dados)

## Como Executar

1. Clone o repositorio
2. Instale as dependencias: `pip install pandas numpy jupyter kaggle python-dotenv`
3. **(Opcao A - Via API)** Crie o arquivo `.env` na raiz com seu token do Kaggle e execute o bloco de carregamento via API no notebook
4. **(Opcao B - Local)** Coloque o arquivo `Shopping Trends And Customer Behaviour Dataset.csv` na pasta do projeto e pule o bloco da API
5. Abra `analise_tendencias.ipynb` e execute as celulas sequencialmente

---

> Projeto desenvolvido para analise exploratoria de dados de tendencias de consumo e comportamento do cliente.
