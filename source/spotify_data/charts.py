import plotly.express as px
import plotly.graph_objects as go

def make_song_rank_changes_chart(data, ch_start, end, ch_artist, ch_title):

    data_x = [c[0] for c in data.order_by("date")]
    data_y = [c[1] for c in data.order_by("date")]

    fig = px.line(template="plotly_dark")
    fig.add_trace(go.Scatter(x=data_x, y=data_y, 
                   name=f"{ch_artist} - {ch_title}", 
                   line=dict(color="#1DB954"), showlegend=True))
    fig.update_layout(title=f"{ch_artist} - {ch_title} rank changes from {ch_start} to {end}", 
    title_x=0.5,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=0.5,
    xanchor="right",
    x=1
    ))

    return fig
