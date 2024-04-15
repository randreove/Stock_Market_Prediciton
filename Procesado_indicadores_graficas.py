import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import talib
import os
import glob
import matplotlib.dates as mdates
import seaborn as sns

# Cargo el Dataset
# df = pd.read_csv('/Users/randreove/Documents/Rafa/VIU/TFM/Codigo/data_scraper/stock_price_scraper/Data/ACS.csv')

# Specify the folder path
folder_path = '/Users/randreove/Documents/Rafa/VIU/TFM/Codigo/data_scraper/stock_price_scraper/Data/'

# Get a list of all CSV files in the folder
csv_files = glob.glob(folder_path + '*.csv')

# Create an empty dictionary to store the dataframes
dataframes = {}

# Create a list to store the describe metrics for each dataframe
describe_metrics = []

# Read each CSV file and store the dataframe in the dictionary
for file in csv_files:
    # Extract the filename without the extension
    filename = file.split('/')[-1].split('.')[0]
    # Read the CSV file and store the dataframe
    dataframes[filename] = pd.read_csv(file)

# Access the dataframes using the filename as the key
for filename, df in dataframes.items():
    print(f"Procesado for {filename}:")
    #print(df.head())
    #print()

    # Elimina las filas en blanco
    df = df[df['Volume'] != 0].dropna()
    
    # Vamos a convertir la fecha en tipo fecha
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Añadimos variables deseadas

    # SMA
    SMA = talib.SMA(df['Close'], timeperiod=14)
    df['SMA'] = SMA

    # EMA
    EMA = talib.EMA(df['Close'], timeperiod=14)
    df['EMA'] = EMA

    # RSI
    RSI = talib.RSI(df['Close'], timeperiod=14)
    df['RSI'] = RSI

    # MACD
    MACD, MACDsignal, MACDhist = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'] = MACD
    df['MACDsignal'] = MACDsignal
    df['MACDhist'] = MACDhist

    # BBANDS
    BBANDS_upper, BBANDS_middle, BBANDS_lower = talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    df['BBANDS_upper'] = BBANDS_upper
    df['BBANDS_middle'] = BBANDS_middle
    df['BBANDS_lower'] = BBANDS_lower

    # STOCH
    STOCH_k, STOCH_d = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['STOCH_k'] = STOCH_k
    df['STOCH_d'] = STOCH_d

    # ADX
    ADX = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['ADX'] = ADX

    print(f'Extraccion for {filename}')
    
    PATH_Extract = '/Users/randreove/Documents/Rafa/VIU/TFM/Codigo/data_scraper/stock_price_scraper/Data/Data_preprocesed/'

    # Create the PATH_Extract folder if it doesn't exist
    if not os.path.exists(PATH_Extract):
        os.makedirs(PATH_Extract)

    # Extract each dataframe to a CSV file in the PATH_Extract folder
    df.to_csv(os.path.join(PATH_Extract, f'{filename}_preprocessed.csv'), index=False)

    
    print(f'Generando graficas {filename}')
    df = df[df['Volume'] != 0].dropna()

        
    # Vamos a representar la SMA y el precio de cierre
    plt.figure(figsize=(16,8))
    plt.title(f'Close Price History, {filename}')  # Fix: Enclose variable names in quotes
    plt.plot(df['Date'], df['Close'], label='Close Price')
    plt.plot(df['Date'], df['SMA'], label='SMA')
    plt.plot(df['Date'], df['EMA'], label='EMA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(loc='upper left')
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format the x-axis as dates
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())  # Automatically set the tick positions
    plt.gcf().autofmt_xdate()  # Rotate and align the x-axis labels
    plt.savefig(f'/Users/randreove/Documents/Rafa/VIU/TFM/Codigo/data_scraper/stock_price_scraper/Data/Figures/{filename}_Close_Price_History.png')
    # plt.show()


    plt.figure(figsize=(12, 6))
    sns.boxplot(x=df['Close'])
    plt.title(f'Box Plot of Close Price, {filename}')
    plt.ylabel('Frequency')
    plt.xlabel('Close Price')
    plt.savefig(f'/Users/randreove/Documents/Rafa/VIU/TFM/Codigo/data_scraper/stock_price_scraper/Data/Figures/{filename}_box_plot.png')
    # plt.show()
        
        

    # Visualize the distribution of numerical variables
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='Close', kde=True)
    plt.title(f'Distribution of Close Price, {filename}')
    plt.xlabel('Close Price')
    plt.ylabel('Frequency')
    plt.savefig(f'/Users/randreove/Documents/Rafa/VIU/TFM/Codigo/data_scraper/stock_price_scraper/Data/Figures/{filename}_distribution.png')
    # plt.show()
    
    
    # print(df['Close'].describe())
    
    # Append the describe metrics for df to the list
    describe_metrics.append(df['Close'].describe()) 
    
    # ADd to the describe_metrics a column with the filename
    describe_metrics[-1]['filename'] = filename
    
# Convert the describe_metrics list to a DataFrame
df_describe_metrics = pd.DataFrame(describe_metrics)

df_describe_metrics['RIC'] = df_describe_metrics['75%'] - df_describe_metrics['25%']

df_describe_metrics['Limite_inferior'] = df_describe_metrics['25%'] - 1.5 * df_describe_metrics['RIC']
df_describe_metrics['Limite_superior'] = df_describe_metrics['75%'] + 1.5 * df_describe_metrics['RIC']

df_describe_metrics['Hay_outliers'] = (df_describe_metrics['Limite_inferior'] > df_describe_metrics['min']) | (df_describe_metrics['Limite_superior'] < df_describe_metrics['max'])


# Export the DataFrame to a CSV file
df_describe_metrics.to_csv('/Users/randreove/Documents/Rafa/VIU/TFM/Codigo/data_scraper/stock_price_scraper/Data/describe_metrics.csv', index=False)

