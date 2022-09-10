#Class supplying a list of graph JSON files for each page.
from DB_manager import DB_manager
import plotly.express as px
import plotly
import pandas as pd
import json

class Analysis:
    def __init__(self):
        self.manager = DB_manager("Data/Database.db")

    def researchers_per_inst_JSON(self):
        researchers_dist = self.manager.researchers_per_inst()
        x_axis = researchers_dist[0]
        y_axis = researchers_dist[1]
        df = pd.DataFrame({
            'Institution': x_axis,
            'Researchers': y_axis,
        })
        fig = px.bar(df, y='Institution', x='Researchers',  barmode='group', orientation='h')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def researchers_per_rating_JSON(self):
        rating_dist = self.manager.researchers_per_rating()
        x_axis = rating_dist[0]
        y_axis = rating_dist[1]
        df = pd.DataFrame({
            'Rating': x_axis,
            'Researchers': y_axis,
        })
        fig = px.bar(df, x='Rating', y='Researchers',  barmode='group')
        fig.update_traces(marker_color='Yellow')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def researcher_rating_by_inst_JSON(self, institution):
        rating_dist = self.manager.researcher_rating_by_inst(institution)
        x_axis = rating_dist[0]
        y_axis = rating_dist[1]
        df = pd.DataFrame({
            'Rating': x_axis,
            'Researchers': y_axis,
        })
        fig = px.bar(df, x='Rating', y='Researchers',  barmode='group')
        fig.update_traces(marker_color='Yellow')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON, y_axis
