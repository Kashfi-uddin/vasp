import pandas as pd
import numpy as np

def extract_elastic_constants(outcar_file):
    with open(outcar_file, 'r') as file:
        lines = file.readlines()
    
    elastic_moduli_section = False
    elastic_moduli_data = []

    for line in lines:
        if 'ELASTIC MODULI (kBar)' in line:
            elastic_moduli_section = True
        elif elastic_moduli_section:
            if 'Direction' in line or '-------' in line:
                continue
            elif line.strip() == '':
                break
            else:
                elastic_moduli_data.append(line.split())

    return elastic_moduli_data

def convert_to_gpa(kbar_data):
    gpa_data = []
    for row in kbar_data:
        direction = row[0]
        values = [float(value) / 10.0 for value in row[1:]]
        gpa_data.append([direction] + values)
    return gpa_data

def save_to_csv(gpa_data, output_file):
    directions = [row[0] for row in gpa_data]
    elastic_data = np.array([row[1:] for row in gpa_data])
    
    # Create a DataFrame
    df = pd.DataFrame(elastic_data, index=directions, columns=['XX', 'YY', 'ZZ', 'XY', 'YZ', 'ZX'])
    
    # Save to CSV
    df.to_csv(output_file)

if __name__ == "__main__":
    outcar_file = 'OUTCAR'  # Path to your OUTCAR file
    output_file = 'elastic_constants.csv'  # Path to the output CSV file
    
    kbar_data = extract_elastic_constants(outcar_file)
    gpa_data = convert_to_gpa(kbar_data)
    save_to_csv(gpa_data, output_file)
    
    print(f"Elastic constants have been saved to {output_file}")
