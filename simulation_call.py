import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

S0 = 100
sigma = 0.3
T = 1
r = 0.05
N = 1000
delta = T/N

def assetPrice():
    B = np.zeros(N+1)
    S = np.zeros(N+1)
    for i in range(N):
        B[i + 1] = B[i] + np.random.normal(0, np.sqrt(delta))
    for i in range(N+1):
        S[i] = S0 * np.exp((r - sigma**2/2) * i * delta + sigma * B[i])
    t = np.linspace(0, T, N+1)
    
    return [t, S]

def callPrice(K):
    d1 = 1/(sigma * np.sqrt(T)) * (np.log(S0 / K) + (r + sigma**2/2) * T)
    d2 = d1 - sigma * np.sqrt(T)
    C = S0 * norm.cdf(d1) - K * np.exp(-(r * T)) * norm.cdf(d2)
    return C


methods = {
    "jour" : 1,
    "semaine" : 2,
    "mois" : 3,
    "debut" : 4,
    "rien" : 5,
}
def couverture(S, method):
    if (method == methods["jour"]):
        j = np.linspace(1, N, 365)
    if (method == methods["semaine"]):
        j = np.linspace(1, N, 52)
    if (method == methods["mois"]):
        j = np.linspace(1, N, 12)
    if (method == methods["debut"]):
        return (norm.cdf(((r + sigma**2/2) * T) / (sigma * np.sqrt(T))) * np.ones(N))
    if (method == methods["rien"]):
        return np.zeros(N)
    H = np.zeros(N)
    d1 = np.zeros(N)
    for i in range(len(j) - 1):
        theta = T - j[i] * delta
        d1[i] = (np.log(S[int(N/(len(j) - 1) * i)] / S0) + ((r + sigma**2/2) * theta)) / \
            (sigma * np.sqrt(theta))
        H[int(N/(len(j) - 1) * i)] = norm.cdf(d1[i])
        for k in range(1, int(N/(len(j) - 1)) + 1):
            H[int(N/(len(j) - 1) * i) + k] = H[int(N/(len(j) - 1) * i)]
    return H
    



