import requests
import pandas as pd

deskripsi_cuaca_id = {
    'clear sky':'cerah',
    'few clouds':'berawan sebagian',
    'broken clouds':'berawan',
    'overcast cloud':'mendung',
    'moderate rain':'hujan sedang',
    'light rain':'hujan ringan',
    'shower rain':'hujan gerimis',
    'rain':'hujan',
    'thunderstrom':'badai petir',
    'snow':'salju',
    'mist':'kabut'
    
}

def ambil_data_cuaca(kota, api_key):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q=Jakarta&appid=61c546708b30fc69cce066996c5305a2'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Error {response.status_code}: {response.text}')
        return None

def analisis_cuaca(data):
    if data is None:
        return None
    
    forecast_list = data.get('list', [])
    dates = []
    temperatures = []
    humidities = []
    weather_description = []
    
    for item in forecast_list:
        date = item['dt_txt'].split(' ')[0]
        dates.append(date)
        temperatures.append(item['main']['temp'])
        humidities.append(item['main']['humidity'])
        desc = item['weather'][0]['description']
        weather_description.append(deskripsi_cuaca_id.get(desc, desc))
        
    df = pd.DataFrame({
        'Tanggal':dates,
        'Suhu (k)': temperatures,
        'kelembapan (%)' : humidities,
        'deskripsi cuaca': weather_description
    })
    
    df['Suhu (C)'] = df['Suhu (k)'] = 273.15
    df = df.drop(columns=['Suhu (k)'])
    
    df_daily = df.groupby('Tanggal').agg({
        'Suhu (C)' : 'mean',
        'kelembapan (%)' : 'mean',
        'deskripsi cuaca' :  lambda x: x.mode()[0]
    }).reset_index()
    
    df_daily.index = df_daily.index + 1
    return df_daily
    
def main():
    kota = input('Masukan Nama Kota: ')
    api_key = '61c546708b30fc69cce066996c5305a2'
    
    data = ambil_data_cuaca(kota, api_key)
    df = analisis_cuaca(data)
    
    if df is not None:
        print(df.head())
        
if __name__ == '__main__':
    main()