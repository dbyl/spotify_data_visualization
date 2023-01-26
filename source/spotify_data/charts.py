import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

def make_song_rank_changes_chart(data, s_artist, s_title):

    data_x = [c[0] for c in data.order_by("date")]
    data_y = [c[1] for c in data.order_by("date")]

    fig = px.line(template="plotly_dark")
    fig.add_trace(go.Scatter(x=data_x, y=data_y, 
                   name=f"{s_artist} - {s_title}", 
                   line=dict(color="#1DB954"), showlegend=True))
    fig.update_layout(xaxis_title="Date", yaxis_title="Ranking",
    title_x=0.5,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=0.5,
    xanchor="right",
    x=1
    ))

    return fig
    
def make_song_rank_changes_comparison_chart(data, data_2, s_artist, s_title, s_artist_2, s_title_2):

    data_x = [c[0] for c in data.order_by("date")]
    data_y = [c[1] for c in data.order_by("date")]

    data_x_2 = [c[0] for c in data_2.order_by("date")]
    data_y_2 = [c[1] for c in data_2.order_by("date")]

    fig = px.line(template="plotly_dark")
    fig.add_trace(go.Scatter(x=data_x, y=data_y, 
                   name=f"{s_artist} - {s_title}", 
                   line=dict(color="#1DB954"), showlegend=True))
    fig.add_trace(go.Scatter(x=data_x_2, y=data_y_2, 
                   name=f"{s_artist_2} - {s_title_2}", 
                   line=dict(color="#1771F1"), showlegend=True))
    fig.update_layout(xaxis_title="Date", yaxis_title="Ranking",
    title_x=0.5,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=0.5,
    xanchor="right",
    x=1
    ))

    return fig

def make_popularity_chart(titles, s_artist):

    titles_counted = Counter(titles)
    titles_counted = dict(sorted(titles_counted.items(), key=lambda item: item[1], reverse=True))

    data_x = list(titles_counted.keys())
    data_y = list(titles_counted.values())
    fig = px.bar(template="plotly_dark")
    fig.add_trace(go.Bar(x=data_x, y=data_y, 
                   name=f"{s_artist}", 
                   marker_color="#1DB954", showlegend=True))
    fig.update_layout(xaxis_title="Titles", yaxis_title="Occurance",
    title_x=0.5,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=0.5,
    xanchor="right",
    x=1
    ))

    return fig

def make_popularity_comparison_chart(titles, titles_2, s_artist, s_artist_2):

    titles_counted = Counter(titles)
    titles_counted = dict(sorted(titles_counted.items(), key=lambda item: item[1], reverse=True))

    titles_counted_2 = Counter(titles_2)
    titles_counted_2 = dict(sorted(titles_counted_2.items(), key=lambda item: item[1], reverse=True))

    data_x = list(titles_counted.keys())
    data_y = list(titles_counted.values())

    data_x_2 = list(titles_counted_2.keys())
    data_y_2 = list(titles_counted_2.values())

    fig = px.bar(template="plotly_dark")
    fig.add_trace(go.Bar(x=data_x, y=data_y, 
                   name=f"{s_artist}", 
                   marker_color="#1DB954", showlegend=True))
    fig.add_trace(go.Bar(x=data_x_2, y=data_y_2, 
                   name=f"{s_artist_2}", 
                   marker_color="#1771F1", showlegend=True))
    fig.update_layout(xaxis_title="Titles", yaxis_title="Occurance",
    title_x=0.5,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=0.5,
    xanchor="right",
    x=1
    ))

    return fig


def make_artist_popularity_map(s_artist, regions_iso, regions_name, share_in_all_streams):

    fig = go.Figure(data=go.Choropleth(
    locations = regions_iso,
    z = share_in_all_streams,
    text = regions_name,
    colorscale = ["#1771F1","#1DB954"],
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = ' %',
    colorbar_title = "Choosen artist share",
    ))

    fig.update_layout(
    title=f"{s_artist}",
    title_x=0.5,
    geo=dict(bgcolor= '#000000', lakecolor='#242e28',
            landcolor='#242e28',
            subunitcolor='grey'),
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    margin=go.layout.Margin(l=45, r=45, t=45, b=45),
    font=dict(color="white"),
    geo_bgcolor="#000000",
    )

    return fig

def make_song_popularity_map(s_artist, s_title, regions_iso, regions_name, share_in_all_streams):

    fig = go.Figure(data=go.Choropleth(
    locations = regions_iso,
    z = share_in_all_streams,
    text = regions_name,
    colorscale = ["#1771F1","#1DB954"],
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = ' %',
    colorbar_title = "Choosen artist share",
    ))

    fig.update_layout(
    title=f"{s_artist} - {s_title}",
    title_x=0.5,
    geo=dict(bgcolor= '#000000', lakecolor='#242e28',
            landcolor='#242e28',
            subunitcolor='grey'),
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    margin=go.layout.Margin(l=45, r=45, t=45, b=45),
    font=dict(color="white"),
    geo_bgcolor="#000000",
    )

    return fig


def make_top_streamed_artist_chart(artist_streams, artists_name, region_name):

    
    data_x = artists_name
    data_y = artist_streams


    fig = px.bar(template="plotly_dark")
    fig.add_trace(go.Bar(x=data_x, y=data_y, 
                  name=f"{region_name}", 
                  marker_color="#1DB954", showlegend=True))
    fig.update_layout(xaxis_title="Titles", yaxis_title="Streams",
    title_x=0.5,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=0.5,
    xanchor="right",
    x=1
    ))

    return fig

def make_top_streamed_artist_comparison_chart(artist_streams, artists_name, region_name,
                                             artist_streams_2, artists_name_2, region_name_2):

    data_x = artists_name
    data_y = artist_streams

    data_x_2 = artists_name_2
    data_y_2 = artist_streams_2




    fig = px.bar(template="plotly_dark")
    fig.add_trace(go.Bar(x=data_x, y=data_y, 
                  name=f"{region_name}", 
                  marker_color="#1DB954", showlegend=True))
    fig.add_trace(go.Bar(x=data_x_2, y=data_y_2, 
                  name=f"{region_name_2}", 
                  marker_color="#1771F1", showlegend=True))
    fig.update_layout(xaxis_title="Titles", yaxis_title="Streams",
    title_x=0.5,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=0.5,
    xanchor="right",
    x=1
    ))

    return fig

def make_top_streamed_song_chart():

    pass

def make_top_streamed_song_comparison_chart():

    pass