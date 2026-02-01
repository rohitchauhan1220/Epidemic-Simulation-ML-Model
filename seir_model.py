import numpy as np
import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import least_squares
import json

class SEIRModel:
    def __init__(self, population=1380000000):
        self.population = population
        self.sigma = 1/5  # incubation ~5 days
        self.gamma_guess = 1/10  # recovery ~10 days
        self.beta_fit = 0.4
        self.gamma_fit = 0.1
        
    def seir_equations(self, y, t, N, beta, sigma, gamma):
        """SEIR differential equations"""
        S, E, I, R = y
        dSdt = -beta * S * I / N
        dEdt = beta * S * I / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return [dSdt, dEdt, dIdt, dRdt]
    
    def run_seir(self, beta, sigma, gamma, N, E0, I0, R0, days):
        """Run SEIR model simulation"""
        S0 = N - E0 - I0 - R0
        y0 = [S0, E0, I0, R0]
        sol = odeint(self.seir_equations, y0, np.arange(days), args=(N, beta, sigma, gamma))
        return sol
    
    def predict(self, days, E0, I0, R0):
        """Generate predictions for given number of days"""
        sol = self.run_seir(self.beta_fit, self.sigma, self.gamma_fit, 
                           self.population, E0, I0, R0, days)
        S, E, I, R = sol.T
        
        return {
            'susceptible': S.tolist(),
            'exposed': E.tolist(),
            'infected': I.tolist(),
            'recovered': R.tolist(),
            'cumulative_infected': (I + R).tolist()
        }

    def fit(self, infected_data, cured_data=None, population=None, sigma=None,
            E0=None, I0=None, R0=None, bounds=(0, 5)):
        """Fit beta and gamma to cumulative infected data using least squares.

        infected_data: 1D array-like of cumulative infected (Confirmed)
        cured_data: optional array-like of cured/recovered values (for R0)
        population: override population if provided
        sigma: incubation rate override
        E0, I0, R0: initial conditions (will be inferred if not provided)
        """
        if population is not None:
            self.population = population
        sigma = sigma or self.sigma

        infected = np.asarray(infected_data)
        t = np.arange(len(infected))

        if I0 is None:
            # try to pick a small positive initial infected
            I0 = float(infected[1]) if len(infected) > 1 else float(infected[0])
        if E0 is None:
            E0 = I0 * 2.0
        if R0 is None:
            if cured_data is not None:
                R0 = float(np.asarray(cured_data)[0])
            else:
                R0 = 0.0

        def residuals(params):
            beta, gamma = params
            pred = self.run_seir(beta, sigma, gamma, self.population, E0, I0, R0, len(t))
            S, E, I, R = pred.T
            infected_pred = I + R
            return infected_pred - infected

        x0 = [self.beta_fit, self.gamma_guess]
        result = least_squares(residuals, x0, bounds=bounds)
        self.beta_fit, self.gamma_fit = result.x
        return result

    def save_params(self, path):
        data = {
            'population': int(self.population),
            'sigma': float(self.sigma),
            'beta': float(self.beta_fit),
            'gamma': float(self.gamma_fit)
        }
        with open(path, 'w') as fh:
            json.dump(data, fh, indent=2)

# Create global model instance
model = SEIRModel()

def predict_seir(days=100, E0=100, I0=50, R0=0):
    """Public function to get predictions"""
    predictions = model.predict(days, E0, I0, R0)
    return json.dumps({
        'status': 'success',
        'predictions': predictions,
        'days': days,
        'beta': model.beta_fit,
        'gamma': model.gamma_fit
    })

if __name__ == '__main__':
    # Example usage
    result = predict_seir(days=100, E0=100, I0=50)
    print(result)
