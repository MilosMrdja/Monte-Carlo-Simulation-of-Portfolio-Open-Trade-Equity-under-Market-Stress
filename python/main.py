import numpy as np
import pandas as pd
import time
from multiprocessing import Pool, cpu_count

# CONF
S0 = 100.0          # Entry price
MU = 0.05     # Ocekivani godisnji prihod 
SIGMA = 0.2  # Standardna devijacija prihoda - volatilnost
DAYS = 252          # Jedna trgovacka godina - vremenski horizont
N_SIMS = 100000   # Ukupan broj Monte Carlo simulacija
POSITION_SIZE = 1000 # Broj jedinica instrumenta
STRESS_THRESHOLD = -0.02 # Prag za aktivaciju stresa (-2%)
STRESS_MULT = 3.0   # Multiplikator volatilnosti tokom stresa
DT = 1 / 252 
STRESS_DURATION = 10

""" Pokrece jednu monte carlo simulaciju"""
def run_single_simulation():
    
    # Prices trenutno nije potreban, korstimo da vidmo istoriju cena
    # prices = np.zeros(DAYS) 
    ote_values = np.zeros(DAYS)
    
    current_price = S0
    stress_countdown = 0
    
    for t in range(DAYS):
        
        # 1. Standardna deivjacija
        if stress_countdown > 0:
            current_sigma = SIGMA * STRESS_MULT
            stress_countdown -= 1
        else:
            current_sigma = SIGMA
        
        # 2. Generisanje random broja (Wienerov proces)
        # np.random.standard_normal je Z u GBM formuli
        z = np.random.standard_normal()
        
        # 3. Nove cena (Geometric Brownian Motion)
        drift_term = (MU - 0.5 * current_sigma**2) * DT
        shock_term = current_sigma * np.sqrt(DT) * z
        
        # Izbegavanje eksponencijalne funkcije za bržu kalkulaciju
        new_price = current_price * np.exp(drift_term + shock_term)
        
        # 4. Provera stresa
        return_rate = (new_price - current_price) / current_price
        if return_rate < STRESS_THRESHOLD and stress_countdown == 0:
            stress_countdown = STRESS_DURATION
            
        current_price = new_price
        # prices[t] = current_price
        
        # 5. Open Trade Equity (OTE)
        ote_values[t] = (current_price - S0) * POSITION_SIZE
        
    return ote_values

""" Pomocna funkcija za paralelno izvrsavanje - chunk"""
def run_chunk(n_in_chunk):
    return [run_single_simulation() for _ in range(n_in_chunk)]

# Sekvencijalno 
def run_sequential():
    print(f"Zapocinjem sekvencijalnu simulaciju ({N_SIMS} putanja)...")
    start_time = time.time()
    
    results = [run_single_simulation() for _ in range(N_SIMS)]
    
    end_time = time.time()
    print(f"Sekvencijalno izvrseno za: {end_time - start_time:.2f} sekundi.")
    return np.array(results), end_time - start_time

# Paralelno
def run_parallel():
    n_cores = cpu_count()
    print(f"Zapocinjem paralelnu simulaciju na {n_cores} jezgara...")
    start_time = time.time()
    
    # Deljenje posla na čankove (Data Decomposition)
    chunk_size = N_SIMS // n_cores
    chunks = [chunk_size] * n_cores
    chunks[-1] += N_SIMS % n_cores # Dodaj ostatak poslednjem jezgru
    
    with Pool(processes=n_cores) as pool:
        # Mapiramo funkciju na čankove
        list_of_chunks = pool.map(run_chunk, chunks)
    
    # Spajanje rezultata (Flattening list)
    results = [path for chunk in list_of_chunks for path in chunk]
    
    end_time = time.time()
    print(f"Paralelno zavrseno za: {end_time - start_time:.2f} sekundi.")
    return np.array(results), end_time - start_time

""" Pisanje u .csv"""
def save_results(results_matrix, filename):
    # results_matrix je oblika (N_SIMS, DAYS) 2d matrix
    df_stats = pd.DataFrame({
        'day': np.arange(DAYS),
        'mean_ote': np.mean(results_matrix, axis=0),
        'min_ote': np.min(results_matrix, axis=0),
        'max_ote': np.max(results_matrix, axis=0),
        'p5_ote': np.percentile(results_matrix, 5, axis=0),
        'p95_ote': np.percentile(results_matrix, 95, axis=0)
    })
    df_stats.to_csv(filename, index=False)
    print(f"Statistika sacuvana u: {filename}")

if __name__ == "__main__":
    # 1. 
    res_seq, time_seq = run_sequential()
    save_results(res_seq, "python_seq_results.csv")
    
    print("-" * 30)
    
    # 2. 
    res_par, time_par = run_parallel()
    save_results(res_par, "python_par_results.csv")
    
    # 3. Analiza ubrzanja
    speedup = time_seq / time_par
    print("-" * 30)
    print(f"Ostvareno ubrzanje (Speedup): {speedup:.2f}x")