import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
# Aqui eu leio o arquivo CSV e já converto a coluna 'date' para formato de data
# Defino a coluna 'date' como index para facilitar a manipulação dos dados 
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
# Agora eu limpo os dados removendo os outliers
# Calculo os percentuais de 2.5% e 97.5% para filtrar apenas os valores no meio
# Isso remove os dias com visualizações muito altas ou muito baixas que podem mudar a análise
df = df[(df.iloc[:, 0] >= df.iloc[:, 0].quantile(0.025)) & (df.iloc[:, 0] <= df.iloc[:, 0].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    # Primeiro eu crio uma figura e um eixo com tamanho específico
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Aqui eu desenho a linha vermelha que mostra as visualizações ao longo do tempo
    # Uso o index_data no eixo X e os valores de página no eixo Y
    ax.plot(df.index, df.iloc[:, 0], color='red', linewidth=1)
    
    # Aqui eu defino os títulos e labels para deixar o gráfico bem explicativo
    # O título deve ser exatamente esse para passar no teste
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    # Primeiro eu faço uma cópia dos dados para não mexer no original
    df_bar = df.copy()
    
    # Filtro o ano e mês de cada data para poder agrupar depois
    # Que ai eu posso calcular médias mensais para cada ano
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    # Group by year and month, then calculate mean
    # Aqui eu agrudo os dados por ano e mês, calculando a média das visualizações
    # O unstack() transforma os meses em colunas, criando uma tabela ano x mês
    df_bar = df_bar.groupby(['year', 'month'])[df_bar.columns[0]].mean().unstack()
    
    # Draw bar plot
    # Aqui crio o gráfico de barras onde cada ano tem barras para cada mês
    # Cada barra representa a média de visualizações daquele mês naquele ano
    fig, ax = plt.subplots(figsize=(10, 6))
    df_bar.plot(kind='bar', ax=ax)
    
    # Defino os labels dos eixos para deixar claro o que cada um representa
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    # Cada cor de barra representa um mês diferente do ano
    ax.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    # Primeiro eu copio os dados para não alterar o original
    df_box = df.copy()
    # Aqui o index é resetado para poder trabalhar com as datas como coluna normal
    df_box.reset_index(inplace=True)
    # Extraio o ano de cada data para criar o primeiro box plot
    df_box['year'] = [d.year for d in df_box.date]
    # Extraio o mês abreviado para o segundo box plot
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # Crio dois gráficos lado a lado para comparar ano e mês
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Year-wise box plot
    # Este gráfico mostra como as visualizações variam entre os anos
    # Cada box representa um ano completo
    sns.boxplot(x='year', y=df_box.columns[1], data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    
    # Month-wise box plot
    # Este gráfico mostra padrões sazonais ao longo dos meses
    # Defino a ordem dos meses para aparecer na sequência correta
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y=df_box.columns[1], data=df_box, order=month_order, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig