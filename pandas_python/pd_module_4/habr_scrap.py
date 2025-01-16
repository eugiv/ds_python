import pandas as pd
import requests
from bs4 import BeautifulSoup


def sub_scraper(
    soup_tag: str,
    tag_attr: str | None,
    soup_feat: str | None,
    soup,
    special_attribute="href",
):
    for i in soup.find_all(soup_tag, {tag_attr: soup_feat}):
        if special_attribute in i.attrs:
            return i[special_attribute]
        else:
            return i.text


def main(keywords: list, page=1):
    articles_data = []

    try:
        for keyword in keywords:
            for page in range(1, page + 1):
                res = requests.get(
                    f"https://habr.com/ru/search/page{page}/?q={keyword}"
                )

                soup = BeautifulSoup(res.text, "lxml")
                article_blocks = soup.find_all("article")

                for article_soup in article_blocks:
                    article_date = sub_scraper(
                        "time", None, None, article_soup, "datetime"
                    )

                    article_title = sub_scraper(
                        "h2", "class", "tm-title tm-title_h2", article_soup
                    )
                    article_link = sub_scraper(
                        "a", "class", "tm-title__link", article_soup
                    )
                    article_text = sub_scraper(
                        "div",
                        "class",
                        "article-formatted-body article-formatted-body article-formatted-body_version-2",
                        article_soup,
                    )
                    article_rating = sub_scraper(
                        "span", "data-test-id", "votes-meter-value", article_soup
                    )

                    article_data = {
                        "date": article_date,
                        "title": article_title,
                        "link": article_link,
                        "text": article_text,
                        "rating": article_rating,
                    }

                    articles_data.append(article_data)

        df = (
            pd.DataFrame(articles_data)
            .sort_values("date", ascending=False)
            .drop_duplicates(subset="link", keep="last")
        )

        def apply_link_header(row):
            if row["link"]:
                return "https://habr.com" + row["link"]

        df["link"] = df.apply(apply_link_header, axis=1)

        return df
    except:
        print("Wrong parameters, try again")


if __name__ == "__main__":
    keywords = ["python", "анализ данных"]
    print(main(keywords, 10))
