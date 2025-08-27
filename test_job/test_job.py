import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1
sheet_url = "https://docs.google.com/spreadsheets/d/1ed1JHrNJEYWJcn-3KiB3CjWzO8E5qHQd-MHM8qQO7a4/export?format=xlsx"

df_cat, df_sales, df_cost = [
    pd.read_excel(sheet_url, sheet_name=sheet, dtype={"Артикул 1C": str, "SKU": str})
    for sheet in ["Каталог", "Продажи", "Себестоимость"]
]

common_df = df_cat.merge(df_sales, how="left", on=["Артикул 1C", "SKU"]).merge(
    df_cost, how="left", on="Артикул 1C"
)

# 2
gp_df = common_df[
    [
        "Дата",
        "Цена продажи,р",
        "Кол-во",
        "Комиссия(% от выручки)",
        "Логистика,р",
        "Себестоимость",
    ]
].copy()

gp_df['Дата'] = pd.to_datetime(gp_df['Дата'])
gp_df = gp_df.sort_values('Дата')

gp_df["Выручка"] = gp_df["Цена продажи,р"] * gp_df["Кол-во"]

gp_df["ВП"] = (
    gp_df["Выручка"] * (1 - gp_df["Комиссия(% от выручки)"] / 100)
    - gp_df["Кол-во"] * (gp_df["Себестоимость"] + gp_df["Логистика,р"])
).round(2)

# 3
gp_df['Неделя'] = gp_df['Дата'].dt.to_period('W').dt.start_time
weekly_plot_df = gp_df.groupby('Неделя')['ВП'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=weekly_plot_df, x='Неделя', y='ВП', marker='o')
plt.title('Валовая прибыль по неделям')
plt.xlabel('Неделя')
plt.ylabel('ВП (руб)')
week_labels = [f"{i+1} н. ({date.strftime('%d.%m')})" for i, date in enumerate(weekly_plot_df['Неделя'])]
plt.xticks(weekly_plot_df['Неделя'], week_labels, rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 4
ma_plot_df = gp_df.groupby('Дата')['ВП'].sum().reset_index()
ma_plot_df['gp_ma_15'] = ma_plot_df['ВП'].rolling(window=15, min_periods=1).mean()

plt.figure(figsize=(12, 6))
sns.lineplot(data=ma_plot_df, x='Дата', y='ВП', marker='o', label='ВП по дням', err_style=None)
sns.lineplot(data=ma_plot_df, x='Дата', y='gp_ma_15', color='red', label='Скользящая средняя 15д', err_style=None)
plt.title('ВП со скользящей средней 15д')
plt.xlabel('Дата')
plt.ylabel('ВП (руб)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()