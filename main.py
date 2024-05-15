from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go


rows = 15
cols = 15 # Qntd de valores
# Gerando os valores aleatórios
data = np.random.rand(rows, cols)

# Criando o DataFrame
df = pd.DataFrame(data, columns=[x for x in range(0, 15)], index=[x for x in range(0, 15)])
# Criar o texto de hover para cada célula do heatmap
hovertext = [[f'Modelo: {df.index[row]}, Poço: {df.columns[col]}, NQDS: {df[row][col]:.2f}' for col in range(cols)] for row in range(rows)]
color_scales = px.colors.named_colorscales()

checklist_options = [{'label': column, 'value': column} for column in df.columns]

app = Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H1("Gráfico Heatmap"),
        html.H3('Seleção de Cores:'),
        dcc.Dropdown(
        id='color-scale-dropdown',
        options=[{'label': scale, 'value': scale} for scale in color_scales],
        value="turbo",
        style={'width': '200px'}
        ),
        html.P("Seleção de Poços", style={'margin-bottom': '0px'}),
        dcc.Checklist(
            id='filtro',
            options=checklist_options,
            value=[column['value'] for column in checklist_options],
            inline=True,
            style={'margin-top': '16px'}
        ),
        html.Div([
            html.P("Habilitar nova iteração", style={'margin': '0'}),
            dcc.Checklist(
                id='toggleheatmap',
                options=[{'label': 'Exibir', 'value': 'show'}],
                value=[]
            ),
        ], style={'display': 'flex', 'margin-top': '16px'}),
        html.Div([
            dcc.Graph(id='heatmap-graph'),
            html.Div(id='novoheatmap')],
            style={'display': 'flex'}
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'flex-direction': 'column', 'align-items': 'center'}),
], style={'height': '100vh'})

@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('color-scale-dropdown', 'value'),
     Input('filtro', 'value')]
)
def update_figure(colorscale, selecao):
    df_filter = df[selecao]

    heatmap = go.Heatmap(
        # Z representa os dados do heatmap
        z=df_filter,
        colorscale=colorscale,
        colorbar=dict(title='Precisão'),
        hovertext=hovertext

    )
    layout = go.Layout(
        title='Gráfico Poços X Modelos',
        xaxis=dict(title='Poços'),
        yaxis=dict(title='Modelos')
    )
    return {'data': [heatmap], 'layout': layout}

@app.callback(
    Output('novoheatmap', 'children'),
    [Input('color-scale-dropdown', 'value'),
     Input('toggleheatmap', 'value'),
     Input('filtro', 'value')]
)
def toggle_extraheatmap(colorscale, value, selecao):
    if 'show' in value:
        df_filter = df[selecao]
        heatmap = go.Heatmap(
            z=df_filter,
            colorscale=colorscale,
            colorbar=dict(title='Precisão'),
            hovertext=hovertext

        )
        layout = go.Layout(
            title='Gráfico Poços X Modelos 2',
            xaxis=dict(title='Poços'),
            yaxis=dict(title='Modelos')
        )
        return dcc.Graph(
            id='extra-heatmap-graph',
            figure={'data': [heatmap], 'layout': layout}
        )
    else:
        return None

if __name__=="__main__":
    app.run(debug=True)

