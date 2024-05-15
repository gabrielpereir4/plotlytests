import dash
from dash import dcc, html
import plotly.graph_objs as go
import numpy as np

# Dados de exemplo para o heatmap
np.random.seed(0)
poços = ['Poço 1', 'Poço 2', 'Poço 3', 'Poço 4']
testes = ['Teste 1', 'Teste 2', 'Teste 3', 'Teste 4']
dados = np.random.rand(len(poços), len(testes))

# Inicialização do app Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Heatmap teste"),
    html.Label('Selecione o esquema de cores:'),
    dcc.Dropdown(
        id='dropdown-colorscale',
        options=[
            {'label': 'Turbo', 'value': 'turbo'},
            {'label': 'Viridis', 'value': 'viridis'},
            {'label': 'Inferno', 'value': 'inferno'},
            {'label': 'Plasma', 'value': 'plasma'},
            {'label': 'Magma', 'value': 'magma'}
        ],
        value='turbo'
    ),
    dcc.Graph(id='heatmap-graph')
])

# Callback para atualizar o gráfico de acordo com a seleção do usuário
@app.callback(
    dash.dependencies.Output('heatmap-graph', 'figure'),
    [dash.dependencies.Input('dropdown-colorscale', 'value')]
)
def update_heatmap(colorscale):
    heatmap = go.Heatmap(
        z=dados,
        x=poços,
        y=testes,
        colorscale=colorscale
    )
    layout = go.Layout(
        title='Heatmap teste',
        xaxis=dict(title='Poços'),
        yaxis=dict(title='Testes')
    )
    return {'data': [heatmap], 'layout': layout}

# Execução do aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)