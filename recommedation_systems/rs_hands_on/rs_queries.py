import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

import pymorphy3


class RsQueries:
    def __init__(self, df):
        self.df = df
        self.morph = pymorphy3.MorphAnalyzer(lang='ru')

    def eda(self):
        self.df = self.df.drop(columns=["loaded_at"])
        print(self.df.info())
        print(self.df.describe())

        queries_count = (
            (
                self.df[["date", "sku", "query"]]
                .groupby(["date", "sku"])
                .count()
                .sort_values(by=["query"], ascending=False)
            )
            .reset_index()
            .rename(columns={"query": "queries_count"})
        )

        def queries_freq_categ(x):
            if x > 40:
                return "high"
            elif x > 10:
                return "med"
            else:
                return "low"

        self.df = self.df.merge(queries_count, on=["date", "sku"], how="inner")
        self.df["sku_freq_category"] = self.df["queries_count"].apply(
            queries_freq_categ
        )
        self.df["query_len"] = self.df["query"].astype(str).str.len()

        self.df["has_order"] = (self.df["order_count"] > 0).astype(int)
        self.df["has_gmv"] = (self.df["gmv"] > 0).astype(int)

        eda_chart_df = self.df.copy()
        agg_method = {
            "view_conversion": lambda x: (x > 0).sum(),
            "unique_search_users": "sum",
            "unique_view_users": "sum",
            "position": "median",
            "query_len": "median",
        }

        eda_chart_df = (
            eda_chart_df.groupby(["date", "sku_freq_category"])
            .agg(agg_method)
            .round(2)
            .reset_index()
        )
        eda_chart_df["search_views_%"] = (
            (eda_chart_df["unique_view_users"] / eda_chart_df["unique_search_users"])
            * 100
        ).round(2)
        eda_chart_df['conversion_case_%'] = (
            (eda_chart_df["view_conversion"] / eda_chart_df["unique_view_users"])
            * 100
        ).round(2)

        return eda_chart_df, self.df

    def eda_plot(self):
        eda_chart_df, _ = self.eda()

        category_order = ['high', 'med', 'low']
        eda_chart_df['sku_freq_category'] = pd.Categorical(
            eda_chart_df['sku_freq_category'],
            categories=category_order,
            ordered=True
        )
        eda_chart_df = eda_chart_df.sort_values('sku_freq_category')

        sns.set_style("whitegrid")
        plt.rcParams.update({'font.size': 11})

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Сравнение категорий SKU по поисковой эффективности', fontsize=16, weight='bold')

        sns.barplot(data=eda_chart_df, x='sku_freq_category', y='position', ax=axes[0, 0], palette='Blues_r')
        axes[0, 0].set_title('Медианная позиция в поисковой выдаче')
        for c in axes[0, 0].containers:
            axes[0, 0].bar_label(c, fmt='%.1f')

        sns.barplot(data=eda_chart_df, x='sku_freq_category', y='unique_search_users', ax=axes[0, 1], palette='Greens')
        axes[0, 1].set_title('Суммарный охват (уникальные пользователи искали)')
        axes[0, 1].ticklabel_format(style='plain', axis='y')

        sns.barplot(data=eda_chart_df, x='sku_freq_category', y='search_views_%', ax=axes[1, 0], palette='Oranges')
        axes[1, 0].set_title('Доля посмотревших от искавших (%)')
        for c in axes[1, 0].containers:
            axes[1, 0].bar_label(c, fmt='%.2f%%')

        sns.barplot(data=eda_chart_df, x='sku_freq_category', y='conversion_case_%', ax=axes[1, 1], palette='Reds')
        axes[1, 1].set_title('Доля конверсии от просмотров (%)')
        for c in axes[1, 1].containers:
            axes[1, 1].bar_label(c, fmt='%.2f%%')

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()

    def normalize_query(self, query):
        q = str(query).lower().strip()
        q = re.sub(r'[^\w\s]', ' ', q)
        q = re.sub(r'\s+', ' ', q)
        return q

    def lemmatize_query(self, query):
        words = self.normalize_query(query).split()
        lemmas = []
        for word in words:
            if len(word) < 2:
                continue
            parsed = self.morph.parse(word)
            if parsed:
                lemma = parsed[0].normal_form
                lemmas.append(lemma)
            else:
                lemmas.append(word)
        return ' '.join(lemmas)

    def cluster_similar_queries(self):
        _, df_sim = self.eda()

        df_sim['query_lemmatized'] = df_sim['query'].apply(self.lemmatize_query)

        df_sim['word_signature'] = df_sim['query_lemmatized'].apply(
            lambda x: ' '.join(sorted(x.split()))
        )

        signature_to_id = {sig: i for i, sig in enumerate(df_sim['word_signature'].unique())}
        df_sim['query_cluster_id'] = df_sim['word_signature'].map(signature_to_id)

        df_sim['query_cluster_repr'] = df_sim.groupby('word_signature')['query'].transform(
            lambda g: min(g, key=lambda x: len(str(x)))
        )

        df_sim = df_sim.drop(columns=['word_signature', 'query_lemmatized', 'query', 'query_cluster_id'])

        agg_method = {
            "gmv": "sum",
            "order_count": "sum",
            "position": "mean",
            "view_conversion": "mean",
            "unique_search_users": "sum",
            "unique_view_users": "sum",
            "query_len": "mean",
            "has_order": "max",
            "has_gmv": "max"
        }
        df_sim = df_sim.groupby(['date','sku','currency','queries_count','sku_freq_category','query_cluster_repr']).agg(agg_method).round(2).reset_index()
        df_sim.to_excel('df_sim.xlsx', index=False)
        return df_sim

if __name__ == "__main__":
    df = pd.read_csv("ozon_product_queries_details.csv")

    rs_model = RsQueries(df)
    # df_mod = rs_model.eda()
    # rs_model.eda_plot()
    rs_model.cluster_similar_queries()
