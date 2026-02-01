import os
import json
import pandas as pd
from seir_model import SEIRModel


def load_national_cases(csv_path):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    national = df.groupby('Date').agg({
        'Confirmed': 'sum',
        'Cured': 'sum',
        'Deaths': 'sum'
    }).sort_index()
    national['New_Cases'] = national['Confirmed'].diff().fillna(national['Confirmed'].iloc[0])
    national = national.fillna(0)
    return national


def main():
    data_path = os.path.join('datasets', 'covid_19_india.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    national = load_national_cases(data_path)
    infected_data = national['Confirmed'].values
    cured_data = national['Cured'].values if 'Cured' in national.columns else None

    POP = 1380000000
    model = SEIRModel(population=POP)

    print('Starting fit on', len(infected_data), 'days of data...')
    res = model.fit(infected_data, cured_data=cured_data)
    print('Optimization success:', bool(res.success))
    print('Fitted beta:', model.beta_fit)
    print('Fitted gamma:', model.gamma_fit)

    os.makedirs('models', exist_ok=True)
    params_path = os.path.join('models', 'params.json')
    model.save_params(params_path)
    print('Saved parameters to', params_path)


if __name__ == '__main__':
    main()
