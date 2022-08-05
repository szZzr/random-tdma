def save_file(data, path):
    import pickle as pkl
    with open(path, 'wb') as file:
        file.write(pkl.dumps(data))


def load_file(path):
    import pickle as pkl
    with open(path, 'rb') as file:
        data = pkl.loads(file.read())
    return data


import matplotlib.pyplot as plt
import numpy as np

def plot(x,y, xlabel:str='', ylabel:str='', title:str=''):
    fig, ax = plt.subplots(figsize=(21, 7))
    # ax.fill_between(x, np.array(y)*1.1, np.array(y)*0.9, alpha=0.1, color="#2492ff")
    ax.plot(x,y, 'o-',  color="#2492ff")
    ax.set_title(title, fontsize=20)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    # ax.legend(loc="best")
    plt.show()
