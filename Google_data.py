import sqlite3
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl

class Google_data:
    def __init__(self, DB_name):
        self.DB_name = DB_name
        self.api_key = " "

    @staticmethod
    def author_results(author_id, api_key):
        author_results_data = []
        params = {
            "api_key": api_key,      # SerpApi API key
            "engine": "google_scholar_author",    # author results search engine
            "author_id": author_id,  # search query
            "hl": "en"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        name = results.get("author").get("name")
        affiliations = results.get("author").get("affiliations")
        interests = results.get("author").get("interests")
        cited_by_graph = results.get("cited_by", {}).get("graph")
        total_citations = results.get("cited_by", {}).get("table")[0].get("citations").get("all")
        co_authors = results.get("co_authors")
        author_results_data.append({
            "name": name,
            "affiliations": affiliations,
            "interests": interests,
            "cited_by_graph": cited_by_graph,
            "co_authors": co_authors,
            "total_citations" : total_citations

        })
        return author_results_data

    @staticmethod
    def all_author_articles(author_id, api_key):
        author_article_results_data = []
        params = {
            "api_key": api_key,     # SerpApi API key
            "engine": "google_scholar_author",   # author results search engine
            "hl": "en",                          # language
            "sort": "pubdate",                   # sort by year
            "author_id": author_id  # search query
        }
        search = GoogleSearch(params)
        articles_is_present = True
        while articles_is_present:
            results = search.get_dict()
            for article in results.get("articles", []):
                title = article.get("title")
                authors = article.get("authors")
                publication = article.get("publication")
                cited_by_value = article.get("cited_by", {}).get("value")
                year = article.get("year")
                author_article_results_data.append({
                    "article_title": title,
                    "article_year": year,
                    "article_authors": authors,
                    "article_publication": publication,
                    "article_cited_by_value": cited_by_value,
                    })
            if "next" in results.get("serpapi_pagination", []):
                search.params_dict.update(dict(parse_qsl(urlsplit(results.get("serpapi_pagination").
                                                                  get("next")).query)))
            else:
                articles_is_present = False
        return author_article_results_data

    def populate_temporary_table(self):
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        cursor.execute("SELECT author_id from Researcher_data")
        author_ids = cursor.fetchall()
        try:
            for author_id in author_ids:
                result_dictionary = Google_data.author_results(author_id[0], self.api_key)
                values = "\'" + author_id[0] + "\', " + str(result_dictionary[0]["total_citations"])
                query = "Insert into citations (author_id, citations) values (" + values + ")"
                cursor.execute(query)

            conn.commit()
        except:
            conn.rollback()
            print("Failed to get citations from Google_Scholar")
            return -1
