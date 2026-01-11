import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

import pymorphy3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RsQueries:
    def __init__(self, df):
        self.df = df
        self.morph = pymorphy3.MorphAnalyzer(lang='ru')

    def eda(self):
        df_eda = self.df.copy()
        df_eda = df_eda.drop(columns=["loaded_at"])
        print(df_eda.info())
        print(df_eda.describe())

        queries_count = (
            (
                df_eda[["date", "sku", "query"]]
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

        df_eda = df_eda.merge(queries_count, on=["date", "sku"], how="inner")
        df_eda["sku_freq_category"] = df_eda["queries_count"].apply(
            queries_freq_categ
        )
        df_eda["query_len"] = df_eda["query"].astype(str).str.len()

        df_eda["has_order"] = (df_eda["order_count"] > 0).astype(int)
        df_eda["has_gmv"] = (df_eda["gmv"] > 0).astype(int)

        eda_chart_df = df_eda.copy()
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

        return eda_chart_df, df_eda

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

        return df_sim

    def baseline_recommendations(self, top_n=5):
        df_sim = self.cluster_similar_queries()

        df_sim['score_seo'] = (
            df_sim['order_count'] * 100 +
            df_sim['view_conversion'] * 10 +
            (1 / (df_sim['position'] + 1)) * 5
        )

        df_sim['ctr_like'] = df_sim['unique_view_users'] / df_sim['unique_search_users'].replace(0, 1)
        df_sim['score_ad'] = (
            df_sim['queries_count'] * 0.1 +
            df_sim['view_conversion'] * 50 +
            (1 / (df_sim['position'] + 1)) * 10 +
            df_sim['ctr_like'] * 100
        )

        seo_recs = df_sim[
            (df_sim['has_order'] == 1) | (df_sim['view_conversion'] > 0)
        ].copy()
        seo_recs = seo_recs.sort_values(['sku', 'score_seo'], ascending=[True, False])
        seo_recs = seo_recs.groupby('sku').head(top_n).reset_index(drop=True)
        seo_recs['recommendation_type'] = 'SEO'

        ad_recs = df_sim[
            (df_sim['queries_count'] >= 30) &  # высокочастотные запросы юзеров
            (df_sim['unique_view_users'] < df_sim['unique_search_users'] * 0.1) &  # низкий охват
            (df_sim['view_conversion'] > 0)  # есть хоть какая-то конверсия
        ].copy()
        ad_recs = ad_recs.sort_values(['sku', 'score_ad'], ascending=[True, False])
        ad_recs = ad_recs.groupby('sku').head(top_n).reset_index(drop=True)
        ad_recs['recommendation_type'] = 'Ad'

        recommendations = pd.concat([seo_recs, ad_recs], ignore_index=True)

        recommendations = recommendations[[
            'sku',
            'query_cluster_repr',
            'recommendation_type',
            'queries_count',
            'position',
            'view_conversion',
            'unique_search_users',
            'unique_view_users',
            'order_count',
            'gmv',
            'score_seo',
            'score_ad'
        ]]

        recommendations.to_excel('baseline_recommendations_extended.xlsx', index=False)

        return recommendations

    def build_text_profiles(self):
        df_sim = self.cluster_similar_queries()

        sku_top_query = df_sim.loc[
            df_sim.groupby('sku')['unique_search_users'].idxmax()
        ][['sku', 'query_cluster_repr']].reset_index(drop=True)

        vectorizer = TfidfVectorizer(
            stop_words=None,
            ngram_range=(1, 2),
            max_features=1000
        )
        tfidf_matrix = vectorizer.fit_transform(sku_top_query['query_cluster_repr'])

        return sku_top_query, tfidf_matrix, vectorizer

    def get_similar_skus(self, target_sku, top_n=5):
        sku_names, tfidf_matrix, _ = self.build_text_profiles()

        target_idx = sku_names[sku_names['sku'] == target_sku].index[0]
        target_vec = tfidf_matrix[target_idx]

        similarities = cosine_similarity(target_vec, tfidf_matrix).flatten()
        sku_names['similarity'] = similarities

        similar = (
            sku_names[sku_names['sku'] != target_sku]
            .sort_values('similarity', ascending=False)
            .head(top_n)
        )

        similar.to_excel('similar_skus_by_top_query.xlsx', index=False)
        return similar[['sku', 'query_cluster_repr', 'similarity']]

    # Модель 3: Коллаборативная фильтрация (Collaborative Filtering)
    def build_interaction_matrix(self):
        df_sim = self.cluster_similar_queries()
        df_sim = df_sim[df_sim['position'] > 0].copy()
        df_sim['relevance'] = 1 / (df_sim['position'] + 1)

        interaction_matrix = df_sim.pivot_table(
            index='query_cluster_repr',
            columns='sku',
            values='relevance',
            fill_value=0
        )

        return interaction_matrix

    def get_similar_skus_collab(self, target_sku, top_n=5):
        interaction_matrix = self.build_interaction_matrix()

        target_vec = interaction_matrix[target_sku].values.reshape(1, -1)
        all_vecs = interaction_matrix.values.T  # транспонируем: теперь строки = SKU
        similarities = cosine_similarity(target_vec, all_vecs).flatten()

        similar_df = pd.DataFrame({
            'sku': interaction_matrix.columns,
            'similarity': similarities
        })

        similar = (
            similar_df[similar_df['sku'] != target_sku]
            .sort_values('similarity', ascending=False)
            .head(top_n)
        )

        similar.to_excel('similar_skus_collab.xlsx', index=False)
        return similar

    # Модель 4: Гибридная модель (Hybrid Model)
    def get_full_cbf_similarity(self):
        sku_names, tfidf_matrix, _ = self.build_text_profiles()
        similarity_matrix = cosine_similarity(tfidf_matrix)
        return pd.DataFrame(
            similarity_matrix,
            index=sku_names['sku'],
            columns=sku_names['sku']
        )

    def get_full_cf_similarity(self):
        interaction_matrix = self.build_interaction_matrix()

        item_vectors = interaction_matrix.T
        similarity_matrix = cosine_similarity(item_vectors)
        return pd.DataFrame(
            similarity_matrix,
            index=item_vectors.index,
            columns=item_vectors.index
        )

    def get_hybrid_recommendations(self, target_sku, top_n=5, weight_cbf=0.6, weight_cf=0.4):
        cbf_sim = self.get_full_cbf_similarity()
        cf_sim = self.get_full_cf_similarity()

        common_skus = cbf_sim.index.intersection(cf_sim.index)
        cbf_scores = cbf_sim.loc[target_sku, common_skus]
        cf_scores = cf_sim.loc[target_sku, common_skus]

        hybrid_scores = weight_cbf * cbf_scores + weight_cf * cf_scores

        hybrid_scores = hybrid_scores.drop(target_sku, errors='ignore')
        top_skus = hybrid_scores.sort_values(ascending=False).head(top_n)

        result = pd.DataFrame({
            'sku': top_skus.index,
            'hybrid_similarity': top_skus.values,
            'cbf_similarity': cbf_scores[top_skus.index].values,
            'cf_similarity': cf_scores[top_skus.index].values
        })

        result.to_excel('hybrid_recommendations.xlsx', index=False)
        return result

if __name__ == "__main__":
    df = pd.read_csv("ozon_product_queries_details.csv")

    rs_model = RsQueries(df)
    # df_mod = rs_model.eda()
    # rs_model.eda_plot()
    # rs_model.cluster_similar_queries()
    # rs_model.get_similar_skus(1614691389, top_n=10)
    # rs_model.get_similar_skus_collab(775129914, top_n=10)
    rs_model.get_hybrid_recommendations(1614691389,top_n=5,weight_cbf=0.6,weight_cf=0.4)
