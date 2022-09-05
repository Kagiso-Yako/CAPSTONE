# class responsible for the creation of string  sqlite queries to be used by other classes. Not responsible for
# THIS CLASS IS NOT RESPONSIBLE FOR DATABASE INTERACTION only the creation of string sqlite queries.

class SQL_queries:
    @staticmethod
    def delete_table(table_name):
        return "DROP TABLE IF EXISTS " + str(table_name)

    @staticmethod
    def create_table_compound_key(table_name, columns: list, primary_key=None):
        # Adding columns to query
        query = "CREATE TABLE " + table_name + " ("
        for column in columns:
            query += column + " ,"
        query = query[0: len(query)-1]

        # Adding primary key: Allows for composite key too
        if primary_key is not None:
            # Composite key support
            if all(x in columns for x in primary_key):
                query += ", PRIMARY KEY ("
                for key in primary_key:
                    query += key + " ,"
                query = query[0: len(query) - 1] + ")"
            # simple key/one column support
            else:
                if primary_key in columns:
                    query += ", PRIMARY KEY (" + primary_key + ")"
        return query + ")"

    @staticmethod
    def create_table(table_name, columns: list):
        # Adding columns to query
        query = "CREATE TABLE " + table_name + " ("
        for column in columns:
            query += column + " ,"
        query = query[0: len(query)-1]
        return query + ")"

    # Method returning insert query. To be used with a list(s) of field values.
    # i.e. cursor.executemany(insert(column_list), recordList) or cursor.executemany(sqlite_insert_query, recordList)
    @staticmethod
    def insert_record(table_name, columns):
        query = "INSERT into " + table_name + " ("
        str_columns = str(columns)
        query += str_columns[1: len(str_columns) - 1] + ") "
        wildcards = len(columns) * "?"
        query += "values (" + wildcards + ");"
        return query

    @staticmethod
    def update_record(table_name, columns, ID, ID_column):
        query = "UPDATE " + table_name + " SET "
        for column in columns:
            query += str(column) + " = ?, "

        query = query[0: len(query) - 2] + " WHERE " + ID_column + " = " + ID + ";"  # removing the last comma
        return query

    @staticmethod
    def delete_record(table_name, ID_column, ID):
        query = "DELETE FROM " + table_name + " WHERE " + ID_column + " = " + ID + ";"
        return query

    @staticmethod
    def delete_subset(table_name, condition):
        query = "DELETE FROM " + table_name + " WHERE (" + condition + ");"
        return query

    # PLEASE PASS LIST INSTEAD OF STRING
    @staticmethod
    def get_table(table_name, columns=None, single_column="", DISTINCT=False):
        query = "select "
        if DISTINCT:
            query += "DISTINCT "

        if columns is not None:
            for column in columns:
                query += column + ","
            query = query[0: len(query) - 1]
        elif single_column != "":
            query += single_column
        else:
            query += " *"

        query += " from " + table_name
        return query

    @staticmethod
    def compare_to_other(column, column_value, operator, conjunction="", negate=False):
        if not negate:
            condition = conjunction + " " + column + " " + operator + " " + str(column_value)
        else:
            condition = conjunction + " " + column + " NOT " + operator + " " + str(column_value)
        return condition

    @staticmethod
    def between_range(column, lower_bound, upper_bound, conjunction="", negation=False):
        if not negation:
            condition = conjunction + " " + column + " BETWEEN " + lower_bound + " AND " + upper_bound
        else:
            condition = conjunction + " NOT " + column + " BETWEEN " + lower_bound + " AND " + upper_bound

        return condition

    @staticmethod
    def count_records(table_name, Distinct=False, columns=None, single_column=""):
        query = "SELECT COUNT("
        if Distinct:
            query += "DISTINCT "

        if columns is not None and not Distinct:
            for column in columns:
                query += column + ", "
            query = query[0: len(query)-2] + ") "
        elif single_column != "":
            query += single_column + ") "
        else:
            if not Distinct:
                query += "*) "
        query += "FROM " + table_name
        return query

    @staticmethod
    def group_by(column):
        group_by = "GROUP BY " + column
        return group_by

    @staticmethod
    def count(column):
        return "COUNT (" + column + ")"
