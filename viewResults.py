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
    
    # Compute Cumulative costs
    df_retailer['costs'] = df_retailer['costs'].cumsum()
    df_wholesaler['costs'] = df_wholesaler['costs'].cumsum()
    df_distributor['costs'] = df_distributor['costs'].cumsum()
    df_factory['costs'] = df_factory['costs'].cumsum()

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 12))
    axes[0, 0].set_title('Retailer', loc='left')
    axes[0, 1].set_title('Wholesaler', loc='left')
    axes[1, 0].set_title('Distributor', loc='left')
    axes[1, 1].set_title('Factory', loc='left')
    
    # Retailer
    axes[0, 0].plot(df_retailer['costs'], color='b')
    ax2 = axes[0, 0].twinx()
    ax2.plot(df_retailer['inventory'], color='g')
    axes[0,0].grid(False)
    ax2.grid(False)
    axes[0, 0].set_xlabel('Weeks')
    axes[0, 0].set_ylabel('Cumulative costs', color='b')
    ax2.set_ylabel('Inventory', color='g')
    ax2.axhline(color='g', lw=0.5)
    
    # Wholesaler
    axes[0, 1].plot(df_wholesaler['costs'], color='b')
    ax2 = axes[0, 1].twinx()
    ax2.plot(df_wholesaler['inventory'], color='g')
    axes[0, 1].grid(False)
    ax2.grid(False)
    axes[0, 1].set_xlabel('Weeks')
    axes[0, 1].set_ylabel('Cumulative costs', color='b')
    ax2.set_ylabel('Inventory', color='g')
    ax2.axhline(color='g', lw=0.5)
    
    # Distributor
    axes[1, 0].plot(df_distributor['costs'], color='b')
    ax2 = axes[1, 0].twinx()
    ax2.plot(df_distributor['inventory'], color='g')
    axes[1, 0].grid(False)
    ax2.grid(False)
    axes[1, 0].set_xlabel('Weeks')
    axes[1, 0].set_ylabel('Cumulative costs', color='b')
    ax2.set_ylabel('Inventory', color='g')
    ax2.axhline(color='g', lw=0.5)
    
    # Factory   
    axes[1, 1].plot(df_factory['costs'], color='b')
    ax2 = axes[1, 1].twinx()
    ax2.plot(df_factory['inventory'], color='g')
    axes[1, 1].grid(False)
    ax2.grid(False)
    axes[1, 1].set_xlabel('Weeks')
    axes[1, 1].set_ylabel('Cumulative costs', color='b')
    ax2.set_ylabel('Inventory', color='g')
    ax2.axhline(color='g', lw=0.5)

    plt.tight_layout(pad=2.4, w_pad=2.0, h_pad=3.0)
    plt.show()

if __name__ == "__main__":
    """
    """
    main()


