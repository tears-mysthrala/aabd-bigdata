import os
import pandas as pd

def main():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    src_csv = os.path.join(cur_dir, "sarrera", "salmentak.csv")
    if not os.path.exists(src_csv):
        src_csv = os.path.expanduser("~/bigdata/materialak/06_Apache_NiFi/salmentak.csv")
    out_csv = os.path.join(cur_dir, "irteera", "salmentak_iragaziak.csv")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    
    # Read CSV skipping comments
    df = pd.read_csv(src_csv, sep=';', comment='#')
    print("Jatorrizko datuak:")
    print(df)
    
    # Filter: Country == 'France' and Units > 1
    iragazia = df[(df['Country'].str.strip() == 'France') & (df['Units'] > 1)]
    print("\nIragazitako datuak (Country == 'France' ETA Units > 1):")
    print(iragazia)
    
    iragazia.to_csv(out_csv, sep=';', index=False)
    print(f"\n✓ Gorde da hemen: {out_csv}")

if __name__ == "__main__":
    main()
