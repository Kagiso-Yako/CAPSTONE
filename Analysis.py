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
        fig.update_layout(title="Researcher distribution by institution", title_x=0.5)
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
        fig = px.bar(df, x='Rating', y='Researchers',  barmode='group', title="Researcher distribution by rating")
        fig.update_layout(title="Researcher distribution by rating", title_x=0.5)
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
        fig.update_layout(title="Institution Researcher distribution by rating", title_x=0.5)
        fig.update_traces(marker_color='Yellow')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON, y_axis

    def rating_pie_chart_JSON(self):
        rating_dist = self.manager.researchers_per_rating()
        rating_x = rating_dist[0]
        rating_y = rating_dist[1]
        df = pd.DataFrame({
            'Rating': rating_x,
            'Researchers': rating_y
        })
        fig = px.pie(df, values='Researchers', names='Rating',  hole=.3)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
