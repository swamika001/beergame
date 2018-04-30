import pandas as pd
import matplotlib.pyplot as plt

def main():
    """
    """
    
    plt.style.use('ggplot')
    
    df_retailer = pd.read_csv('retailer.csv', index_col=0)
    df_wholesaler = pd.read_csv('wholesaler.csv', index_col=0)           
    df_distributor = pd.read_csv('distributor.csv', index_col=0)
    df_factory = pd.read_csv('factory.csv', index_col=0)

    fig, axes = plt.subplots(nrows=2, ncols=2)
    axes[0, 0].set_title('Retailer')
    axes[0, 1].set_title('Wholesaler')
    axes[1, 0].set_title('Distributor')
    axes[1, 1].set_title('Factory')
    
    l1,l2 = axes[0, 0].plot(df_retailer)
    axes[0, 1].plot(df_wholesaler)
    axes[1, 0].plot(df_distributor)
    axes[1, 1].plot(df_factory)
    
    fig.legend((l1, l2), ('Costs', 'Inventory Level'), 'upper left')
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    """
    """
    main()


