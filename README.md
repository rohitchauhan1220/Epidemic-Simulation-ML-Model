# SEIR Model - Standalone Application

A simple, direct SEIR model for COVID-19 epidemic simulation without backend server complexity.

## Quick Start

### Option 1: Direct HTML (Recommended)
Simply open `index.html` in your browser - no installation needed!

```
Double-click: index.html
```

### Option 2: Run with Python
```bash
python seir_model.py
```

## Files

- **index.html** - Complete standalone dashboard (all-in-one file)
- **seir_model.py** - Python SEIR model implementation (optional)
- **finalmlproject.py** - Original data analysis script

## Features

✅ **No Backend Required** - Pure HTML/CSS/JavaScript
✅ **Instant Predictions** - Click and see results immediately
✅ **Interactive Charts** - Real-time visualization
✅ **Responsive Design** - Works on all devices
✅ **Simple Controls** - Easy parameter adjustment

## How It Works

1. Open `index.html` in your browser
2. Set initial conditions (E0, I0, R0)
3. Choose prediction days
4. Click "Generate Predictions"
5. View results in charts

## Model Parameters

- **β (Beta)**: 0.4 - Transmission rate
- **γ (Gamma)**: 0.1 - Recovery rate
- **σ (Sigma)**: 0.2 - Incubation rate
- **Population**: 1.38 billion (India)

## SEIR Equations

```
dS/dt = -β·S·I/N
dE/dt = β·S·I/N - σ·E
dI/dt = σ·E - γ·I
dR/dt = γ·I
```

Where:
- S = Susceptible
- E = Exposed
- I = Infected
- R = Recovered
- N = Total Population
