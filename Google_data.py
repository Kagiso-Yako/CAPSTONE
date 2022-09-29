import sqlite3
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl

class Google_data:
    def __init__(self, DB_name):
        self.DB_name = DB_name
        self.citations = []
        self.api_key = "57025192178ecbcd0a32e0f3919ac583c16c3bcd2d323723af054a1d97f5d3cd"
        self.api_calls_remaining = 75
        # for testing during load shedding

    def find_best_fit(self, query, initials, surname, institution, primary_research, secondary_research):
        best_fit = None
        maxim = 0
        primary_fields = primary_research.split(";")
        secondary_fields = secondary_research.split(";")
        profiles = self.get_profiles(query)

        for profile in profiles:
            hits = 0

            # Some attributes are more important than others
            if surname in profile.get("name"):
                hits += 1000

            for i in range(len(initials)):
                names = profile.get("name").split(" ")
                if names[i][0] == initials[i] or names[len(initials)-i-1][0] == initials[i]:
                    hits += 100

            if institution in profile.get("affiliations"):
                hits += 10

            for i in range(len(primary_fields)):
                if profile.get("interests") is not None:
                    if primary_fields[i] in profile.get("interests"):
                        hits += 1

                if profile.get("interests") is not None:
                    if secondary_fields[i] in profile.get("interests"):
                        hits += 1

            if hits > maxim:
                best_fit = profile
                maxim = hits

        return best_fit, maxim  # Maxim: Maximum and is used to measure the degree of certainty.

    def get_profiles(self, search_query):
        params = {
            "api_key": self.api_key,
            "engine": "google_scholar_profiles",  # profile results search engine
            "mauthors": search_query  # search query
        }
        search = GoogleSearch(params)
        profile_results_data = []
        profiles_is_present = True
        while profiles_is_present:
            profile_results = search.get_dict()
            for profile in profile_results.get("profiles", []):
                name = profile.get("name")
                author_id = profile.get("author_id")
                affiliations = profile.get("affiliations")
                interests = profile.get("interests")
                profile_results_data.append({
                    "name": name,
                    "author_id": author_id,
                    "affiliations": affiliations,
                    "interests": interests
                })

            if "next" in profile_results.get("pagination", []):
                search.params_dict.update(
                    dict(parse_qsl(urlsplit(profile_results.get("pagination").get("next")).query)))
            else:
                profiles_is_present = False
        return profile_results_data

    def author_results(self, author_id):
        author_results_data = []
        params = {
            "api_key": self.api_key,      # SerpApi API key
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

    def all_author_articles(self, author_id):
        author_article_results_data = []
        params = {
            "api_key": self.api_key,     # SerpApi API key
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

    def get_citations(self):
        return self.citations

    def populate_citations(self):
        temp_citations = []
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        cursor.execute("SELECT author_id from Researcher_data limit 1")
        author_ids = cursor.fetchall()
        for author_id in author_ids:
            result_dictionary = self.author_results(author_id[0])
            temp_citations.append({"author_id" : author_id,
                                   "citations": result_dictionary[0].get("total_citations"),
                                   "cited_by_graph" : result_dictionary[0].get("cited_by_graph")})

        self.citations = temp_citations
