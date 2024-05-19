import numpy as np

def get_MM(price_tab, window):
    average_tab = []
    for i in range(len(price_tab)):
        if i >= window - 1:  
            average = np.mean(price_tab[i - window + 1 : i + 1])
            average_tab.append(average)
        else:
            average_tab.append(None) 
    return average_tab 