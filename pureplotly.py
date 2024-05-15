import pandas as pd
import numpy as np
import plotly.express as px

# Em plotly puro tá funcionando!

def main():
    rows = 150
    cols = 150
    # Gerando os valores aleatórios
    data = np.random.rand(rows, cols)

    # Criando o DataFrame
    df = pd.DataFrame(data, columns=[x for x in range(0, cols)], index=[x for x in range(0, rows)])
    color_scales = px.colors.named_colorscales()

    fig = px.imshow(df, text_auto=True,
                    labels=dict(x="Modelos", y="Poços", color="Precisão"),
                    color_continuous_scale="turbo")
    fig.show()

main()