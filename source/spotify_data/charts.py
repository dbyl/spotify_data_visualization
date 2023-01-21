import plotly.express as px
import plotly.graph_objects as go

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