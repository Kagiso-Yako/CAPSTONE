import sqlite3
from flask import render_template, request
from Graph_JSONs import Analysis
from DB_auto_setup import DB_auto_setup
from DB_manager import DB_manager
from SQL_queries import SQL_queries

# Global variables
# Defines the columns for the csv file and the columns for the NRF researchers table
#from googleScholarOperations import handle_query
#from test import notdash
from googleScholarOperations import handle_query


class Webpage_builder:
    def __init__(self):
        self.secondary_options = []
        self.primary_options = []
        self.specializations_options = []
        self.table_name = "Researchers"
        excel_sheet_name = 'Current Rated Researchers (Webs'
        csv_file = "Data/DB.csv"
        self.NRF_database_file = "Data/Database.db"
        specializations = ["Artificial Intelligence",
                           "Computer vision",
                           "Natural language processing",
                           "Artificial Neural Networks",
                           "Robotics",
                           "Deep learning",
                           "Knowledge representation and reasoning",
                           "Search methodologies",
                           "Machine learning",
                           "Reinforcement learning"]
        top_institutions = ["University of Cape Town",
                            "University of the Witwatersrand",
                            "University of Pretoria",
                            "University of KwaZulu-Natal",
                            "Stellenbosch University"]
        self.columns = ["id INTEGER primary key autoincrement",
                   "Surname TEXT",
                   "Initials TEXT",
                   "Title TEXT",
                   "Institution TEXT",
                   "Rating TEXT",
                   "Rating_Start DATE",
                   "Rating_Ending DATE",
                   "PrimaryResearch TEXT",
                   "SecondaryResearch TEXT",
                   "Specializations TEXT"]

        self.columns_csv = ["Surname",
                       "Initials",
                       "Title",
                       "Institution",
                       "Rating",
                       "Rating_Start",
                       "Rating_Ending",
                       "PrimaryResearch",
                       "SecondaryResearch",
                       "Specializations"]

        self.auto = DB_auto_setup(self.NRF_database_file, excel_sheet_name, self.columns_csv, csv_file,
                                  self.table_name, self.columns, specializations=specializations)

        self.my_manager = DB_manager(self.NRF_database_file, specializations)
        self.my_JSONs = Analysis(self.NRF_database_file, specializations)

        self.populate_options()
    #
    #
    #
    #
    #
    # Page generation methods
    #
    #
    #
    #
    #
    #
    #
    #
    #

    def homepage(self):
        if request.method == "POST":
            query = request.form["query"]
            queryType = request.form.get('Querytype')
            #results = handle_query(queryType, query)
            results = []
            return render_template("results.html", results=results)
        return render_template("index.html")

    def researchers_page(self):
        rows = []
        rating_dist_JSON = self.my_JSONs.researchers_per_rating_JSON()
        options_column = ["Surname", "Institution"]
        options = []
        try:
            conn = sqlite3.connect(self.NRF_database_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            try:
                cursor.execute(SQL_queries.get_table(self.table_name))
                rows = cursor.fetchall()
            except sqlite3.Error:
                print("Unable to obtain rows")
            options = self.fetch_options("Researchers", options_column)
        except sqlite3.Error:
            print("Could not connect to database!")
        finally:
            if rows is not None:
                return render_template("researchers.html", rows=rows, options=options, sec=self.secondary_options,
                                       prim=self.primary_options, spec=self.specializations_options,inst=self.institution_options, surn=self.researcher_options,
                                       rating_dist=rating_dist_JSON)
            else:
                return render_template("Error_page.html")

    def institutions_page(self):
        rows = None
        options = None
        conn = sqlite3.connect(self.NRF_database_file)
        conn.row_factory = sqlite3.Row
        try:

            cursor = conn.cursor()
            options = self.fetch_options("Institutions", option_columns=["Institution", "Location"])
            try:
                cursor.execute(SQL_queries.institutions_table() + " GROUP BY Institutions.institution ")
                rows = cursor.fetchall()
            except sqlite3.Error:
                print("Unable to obtain rows")
        except sqlite3.Error:
            print("Could not connect to database!")
        if rows is not None :
            res_vs_inst_JSON, institutions = self.my_JSONs.researchers_per_inst_JSON()
            return render_template("institutions.html", res_vs_I=res_vs_inst_JSON, rows=rows, options=options)
        return render_template("Error_page.html")

    def TrendsAndAnalysis_page(self):
        JSON_general = self.my_JSONs.researchers_per_rating_JSON()
        JSON_general_prev = self.my_JSONs.researchers_per_rating_JSON(table="PreviousResearchers")
        JSON_institution, institutions = self.my_JSONs.researchers_per_inst_JSON()
        ratings_pie_JSON = self.my_JSONs.rating_pie_chart_JSON()
        ratings_per_topic = self.my_JSONs.researchers_per_topic_JSON("Artificial intelligence")
        ratings = self.my_JSONs.get_ratings_list()
        researchers_per_field = self.my_JSONs.researchers_per_field_JSON()

        # top institutions graphs
        # "Researcher Instittuion distribution by topic: "
        specializations_per_inst = self.my_JSONs.specialization_top_inst_JSON("Artificial intelligence")
 
        # "Researcher distribution by institution: "
        ratings_per_inst = self.my_JSONs.rating_top_inst_JSON("University of Cape Town")

        # "Researcher distribution by top institution"
        researchers_per_inst = self.my_JSONs.researchers_per_top_inst_JSON()

        # "Researcher distribution by primary research"
        researchers_per_primary = self.my_JSONs.primary_research_top_inst_JSON()



        rating_percentages = []
        for rating in ratings:
            rating_percentages.append(round(int(rating) / sum(ratings) * 100))
        maxi = round(max(ratings) / sum(ratings) * 100)
        mini = round(min(ratings) / sum(ratings) * 100)
        rating_categories = ["A", "B", "C", "P", "Y"]
        min_rating = rating_categories[ratings.index(min(ratings))]
        max_rating = rating_categories[ratings.index(max(ratings))]
        rows = None
        conn = sqlite3.connect(self.NRF_database_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(SQL_queries.get_table(self.table_name))
            rows = cursor.fetchall()
        except sqlite3.Error:
            print("Unable to obtain rows")
        return render_template("TrendsAndAnalysis.html", general=JSON_general, institution=JSON_institution,
                               rating_pie=ratings_pie_JSON, ratings=ratings, rating_p=rating_percentages,
                               sum=sum(ratings), prev_JSON=JSON_general_prev,
                               specialization_dist=researchers_per_field, ratings_per_topic=ratings_per_topic,
                               specializations_per_inst=specializations_per_inst, ratings_per_inst=ratings_per_inst,
                               researchers_per_inst=researchers_per_inst, researchers_per_primary=researchers_per_primary,
                               max=maxi,min=mini, min_r=min_rating, max_r=max_rating, rows=rows, institutions=institutions[0:10])

    def publications_page(self):
        if request.method == "POST":
            query = request.form["query"]
            queryType = request.form.get('Querytype')
            handle_query(queryType, query)
            return handle_query(queryType, query)

        return render_template("publications.html")

    def render_institution_page(self, institution):
        institution = institution.replace('+', ' ')
        logo_image = "static/images/" + institution + ".png"
        institution_dist, values = self.my_JSONs.researcher_rating_by_inst_JSON(institution)
        my_sum = 0
        rows = None
        try:
            conn = sqlite3.connect(self.NRF_database_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            quoted_inst = "\"" + institution + "\""
            cursor.execute(SQL_queries.get_table(self.table_name) + SQL_queries.compare_to_other("Institution",
                                                                                            quoted_inst, "=",
                                                                                            prefix="WHERE"))
            rows = cursor.fetchall()
            my_sum = sum(values)
        except sqlite3.Error:
            print("Failed to connect to database for the creation of institution.html")
        if rows is not None:
            return render_template("institution.html", institution_dist=institution_dist, institution=institution,
                                   sum=my_sum, values=values, rows=rows, logo_image=logo_image)
        else:
            return render_template("Error_page.html")

    def render_researcher_page(self, my_id):
        rows = []
        prim = []
        sec = []
        spec = []
        logo_image = ""
        profile_image = "static/images/profile.png"

        try:
            conn = sqlite3.connect(self.NRF_database_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = "SELECT * FROM Researchers WHERE id = '" + my_id + "'"
            cursor.execute(query)
            rows = cursor.fetchall()
            prim = rows[0]["PrimaryResearch"].split(";")
            print(prim)
            sec = rows[0]["SecondaryResearch"].split(";")
            spec = rows[0]["Specializations"].split(";")
            institution = rows[0]["Institution"].replace('+', ' ')
            logo_image = "static/images/" + institution + ".png"
            print(logo_image)
            print(spec)
        except sqlite3.Error:
            print("Failed to connect to database for the creation of researcher.html")
        if len(rows) != 0:
            return render_template("researcher.html", id=my_id, surname=rows[0]["Surname"],
                                   rows=rows, profile_image=profile_image, sec=sec, prim=prim, spec=spec,
                                   logo=logo_image)
        else:
            return render_template("Error_page.html")

    def search_institutions(self, method, item):
        if method == "GET":
            rows = None
            try:
                conn = sqlite3.connect(self.NRF_database_file)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(SQL_queries.institutions_table_search_query(item))
                rows = cursor.fetchall()

            except sqlite3.Error:
                print("sqlite3.Error: Could not execute search.")
            if rows is not None:
                if len(rows) > 0:
                    return render_template("search_institutions.html", rows=rows, length=len(rows))
                else:
                    return render_template("NoItemsFound.html")
            else:
                return render_template("Error_page.html")

    def search_researchers(self):
        if request.method == "GET":
            rows = None
            try:
                item = request.args.get("researcher_search")
                operators = ["LIKE"] * len(self.columns_csv)
                wild_card_wrapped_item = "%" + item + "%"
                query = SQL_queries.get_subset(self.table_name, self.columns_csv, operators,
                                               to_one=wild_card_wrapped_item, wrap=True)
                conn = sqlite3.connect(self.NRF_database_file)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()

            except sqlite3.Error:
                print("sqlite3.Error: Could not execute search.")
            finally:
                if rows is not None:
                    if len(rows) > 0:
                        return render_template("search_researchers.html", rows=rows, length=len(rows))
                    else:
                        return render_template("NoItemsFound.html")
                else:
                    return render_template("Error_page.html")
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #Supporting methods
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

    def graph_callback(self):
        field = request.args.get('data')
        return self.my_JSONs.researchers_per_topic_JSON(field)
    
    def graph2_callback(self):
        field = request.args.get('data')
        return self.my_JSONs.specialization_top_inst_JSON(field)

    def graph3_callback(self):
        institution = request.args.get('data')
        return self.my_JSONs.rating_top_inst_JSON(institution)

    def fetch_options(self, table_n , option_columns):
        conn = sqlite3.connect(self.NRF_database_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        options = []
        for i in range(len(option_columns)):
            try:
                cursor.execute(SQL_queries.get_table(table_n, single_column=option_columns[i], DISTINCT=True))
                options.append(cursor.fetchall())

            except sqlite3.Error:
                print("Unable to obtain " + option_columns[i] + " options!")
        return options

    def research_fields(self, research_type):
        conn = sqlite3.connect(self.NRF_database_file)
        cursor = conn.cursor()

        query = "SELECT " + research_type + " FROM Researchers"

        cursor.execute(query)
        data = cursor.fetchall()

        research_options = []

        for item in data:
            string_fields = str(item[0])
            fields = string_fields.split(";")

            for option in fields:
                if option not in research_options:
                    research_options.append(option)

        research_options.sort()

        return research_options

    def populate_options(self):
        self.primary_options = self.research_fields("PrimaryResearch")
        self.secondary_options = self.research_fields("SecondaryResearch")
        self.specializations_options = self.research_fields("Specializations")
        self.institution_options = self.my_manager.get_institutions()
        self.researcher_options = self.my_manager.get_researchers()
        
