# Kagiso Yako
# 31/08/2022
# Class for executing high level sqlite instructions and database interaction and management.

import sqlite3
from SQL_queries import SQL_queries


class DB_manager:
    def __init__(self, DB_name, specializations):
        self.DB_name = DB_name
        self.AI_fields = specializations
        self.AI_fields.sort()

    def researchers_per_inst(self):
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        cursor.execute("SELECT Institution, count(Institution) FROM Researchers group by institution " +
                       "order by count(institution) DESC;")
        count_inst = cursor.fetchall()
        institutions = []
        frequencies = []
        for i in range(len(count_inst)):
            institutions.append(count_inst[i][0])
            frequencies.append(count_inst[i][1])
        return institutions, frequencies

    def researchers_per_rating(self, table="Researchers"):
        frequencies = [0, 0, 0, 0, 0]
        ratings = ["A", "B", "C", "P", "Y"]
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        query = SQL_queries.get_table(table, columns=["Rating", "count(rating)"])
        query += SQL_queries.group_by("Rating")
        cursor.execute(query)
        values = cursor.fetchall()
        for i in range(len(ratings)):
            if values[i][0] is not None:
                frequencies[ratings.index(values[i][0])] = (values[i][1])
        return ratings, frequencies

    def researcher_rating_by_inst(self, institution):
        frequencies = [0, 0, 0, 0, 0]
        ratings = ["A", "B", "C", "P", "Y"]
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        query = "SELECT rating, count(rating) from researchers WHERE "
        query += SQL_queries.compare_to_other("Institution", "\"" + institution + "\"", "=", )
        query += SQL_queries.group_by("Rating")
        cursor.execute(query)
        values = cursor.fetchall()
        print(values)
        for i in range(len(values)):
            frequencies[ratings.index(values[i][0])] = (values[i][1])

        return ratings, frequencies

    def researchers_per_specialization(self):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        field_X = []
        num_researchers_Y = []

        for field in self.AI_fields:
            query = "SELECT Count(Surname) FROM Researchers "
            query += "WHERE Specializations LIKE  '%" + field + "%';"

            cursor.execute(query)
            data = cursor.fetchall()

            field_X.append(field)
            num_researchers_Y.append(data[0][0])

        return field_X, num_researchers_Y

    def researcher_dist_by_specialization(self, field):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        ratings = ["A", "B", "C", "P", "Y"]
        rating_distribution = [0] * len(ratings)
        query = "SELECT rating ,Count(Rating) FROM Researchers "
        query += "WHERE Specializations LIKE '%" + field + "%' "
        query += "GROUP BY Rating"

        cursor.execute(query)
        data = cursor.fetchall()
        for i in range(len(data)):
            rating_distribution[ratings.index(data[i][0])] = data[i][1]
        return ratings, rating_distribution

    def specialization_dist_by_inst(self, inst):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        specialization_distribution = []

        for field in self.AI_fields:
            query = "SELECT  Specializations, Count(Specializations) FROM Researchers "
            query += "WHERE Institution LIKE '%" + inst + "%'  AND specializations LIKE %" + field + "% "
            query += "GROUP BY Institution"

            cursor.execute(query)
            data = cursor.fetchall()

            specialization_distribution.append(data)

        return self.AI_fields, specialization_distribution

    def get_researchers(self):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        query = "SELECT Surname FROM Researchers"

        cursor.execute(query)
        data = cursor.fetchall()

        researchers = []

        for item in data:
            surname = str(item[0])
            researchers.append(surname)

        return researchers

    def get_institutions(self):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        query = "SELECT DISTINCT Institution FROM Researchers"

        cursor.execute(query)
        data = cursor.fetchall()

        institutions = []

        for item in data:
            surname = str(item[0])
            institutions.append(surname)

        return institutions

    ############
    
    def specialization_dist_by_top_inst(self, field):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
    
        institution = ["University of Cape Town",
                           "University of the Witwatersrand",
                    "University of Pretoria",
                    "University of KwaZulu-Natal",
                    "Stellenbosch University"]
    
        #topic = []
        #specialization_distriution = []
    
        institution_frequency = {}
    
        institutions = []
        frequency = []
    
        query = "SELECT  Institution, Count(Institution) FROM Researchers "
        query += "WHERE Institution = 'University of Cape Town' AND Specializations LIKE '%" + field + "%' "
        query += "OR Institution = 'University of the Witwatersrand' AND Specializations LIKE '%" + field + "%' "
        query += "OR Institution = 'University of Pretoria'AND Specializations LIKE '%" + field + "%' "
        query += "OR Institution = 'University of KwaZulu-Natal' AND Specializations LIKE '%" + field + "%' "
        query += "OR Institution = 'Stellenbosch University' AND Specializations LIKE '%" + field + "%' "
        query += "GROUP BY Institution"
    
        #print(query)
        cursor.execute(query)
        data = cursor.fetchall()
    
        #print(field)
        #print_data(data)
    
        for item in (data):
            institutions.append(item[0])
            frequency.append(item[1])
    
        for i in institution:
            if i not in institutions:
                institutions.append(i)
                frequency.append(0)
    
        for i in range(len(institutions)):
            institution_frequency[institutions[i]] = frequency[i]
    
        institutions = institution
    
        for i in range(len(institutions)):
            frequency[i] = institution_frequency[institutions[i]]
    
    
        return institutions, frequency

    
    def researcher_dist_by_top_inst(self, institution):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
    
        #inst = []
        #researcher_distribution = []
    
        rating = ["A", "B", "C", "P", "Y"]
    
        ratings = []
        frequency = []
    
    
    
        query = "SELECT Rating, Count(Rating) FROM Researchers "
        query += "WHERE Institution = '" + institution + "' "
        query += "GROUP BY Rating;"
    
        #print(query)
        cursor.execute(query)
        data = cursor.fetchall()
    
        rating_frequency = {}
    
        for item in (data):
            ratings.append(item[0])
            frequency.append(item[1])
    
        for i in rating:
            if i not in ratings:
                ratings.append(i)
                frequency.append(0)
    
        for i in range(len(ratings)):
            rating_frequency[ratings[i]] = frequency[i]
    
        ratings.sort()
    
        for i in range(len(ratings)):
            frequency[i] = rating_frequency[ratings[i]]
    
    
        return  ratings, frequency

    
    def researchers_per_top_inst(self):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        institutions = []
        frequency = []

        query = "SELECT Institution, Count(Institution) FROM Researchers "
        query += "WHERE Institution = 'University of Cape Town' "
        query += "OR Institution = 'University of the Witwatersrand' "
        query += "OR Institution = 'University of Pretoria' "
        query += "OR Institution = 'University of KwaZulu-Natal' "
        query += "OR Institution = 'Stellenbosch University' "
        query += "GROUP BY Institution;"

        #print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        
        #print_data(data)

        for item in (data):
            institutions.append(item[0])
            frequency.append(item[1])

        return  institutions, frequency


    def primary_research_dist_by_top_inst(self):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        primary = []
        frequency = []

        query = "SELECT PrimaryResearch, Count(PrimaryResearch) FROM Researchers "
        query += "WHERE Institution = 'University of Cape Town' AND PrimaryResearch IS NOT NULL "
        query += "OR Institution = 'University of the Witwatersrand' AND PrimaryResearch IS NOT NULL "
        query += "OR Institution = 'University of Pretoria' AND PrimaryResearch IS NOT NULL "
        query += "OR Institution = 'University of KwaZulu-Natal' AND PrimaryResearch IS NOT NULL "
        query += "OR Institution = 'Stellenbosch University' AND PrimaryResearch IS NOT NULL  "
        query += "GROUP BY PrimaryResearch;"

        #print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        
        #print_data(data)

        for item in (data):
            primary.append(item[0])
            frequency.append(item[1])

        return  primary, frequency
    
    ##########

    # ai_topics is an array of different AI topics, ["Artificial Intelligence", "Machine Learning", "Deep learning",..]
    def clean_data(self, ai_topics):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        query = "DELETE FROM Researchers"

        specializations = " WHERE "
        primary = " AND "
        secondary = " AND "

        for index in range(len(ai_topics)):

            if index == len(ai_topics) - 1:

                specializations += "Specializations NOT LIKE '%" + ai_topics[index] + "%'"
                primary += "PrimaryResearch NOT LIKE '%" + ai_topics[index] + "%'"
                secondary += "SecondaryResearch NOT LIKE '%" + ai_topics[index] + "%'"

            else:

                specializations += "Specializations NOT LIKE '%" + ai_topics[index] + "%' AND "
                primary += "PrimaryResearch NOT LIKE '%" + ai_topics[index] + "%' AND "
                secondary += "SecondaryResearch NOT LIKE '%" + ai_topics[index] + "%' AND "

        query += specializations
        query += primary
        query += secondary

        query += " OR Specializations IS NULL "
        query += " OR PrimaryResearch IS NULL "
        query += " OR SecondaryResearch IS NULL"

        # print(query)
        cursor.execute(query)

        query2 = "SELECT * FROM Researchers"
        cursor.execute(query2)
        new_data = cursor.fetchall()

        return new_data  # returns a new table after the cleaning the data
