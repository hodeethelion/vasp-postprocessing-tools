from pymatgen.core import Structure 
from pymatgen.io.vasp import Xdatcar, Outcar, Oszicar
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
def read_magnetization_from_outcar(outcar_path, n_ions=144):
    """
    Fast reading of magnetization 'tot' column from OUTCAR file.
    
    Parameters:
    -----------
    outcar_path : str
        Path to OUTCAR file
    n_ions : int
        Number of ions in the system (default: 144)
    
    Returns:
    --------
    magnetization : np.ndarray
        Shape (n_ionic_steps, n_ions) containing 'tot' magnetization for each ion
    """
    magnetization_all_steps = []
    
    with open(outcar_path, 'r') as f:
        lines = f.readlines()
    
    i = 0
    n_lines = len(lines)
    
    while i < n_lines:
        line = lines[i]
        # Look for the magnetization block marker
        if "magnetization (x)" in line:
            i += 4  # Skip: blank line, header line, dashed line -> ion 1
            mag_step = []
            
            # Read magnetization for each ion
            for _ in range(n_ions):
                if i >= n_lines:
                    break
                parts = lines[i].split()
                if len(parts) >= 5:
                    try:
                        tot_mag = float(parts[4])  # 'tot' column is the 5th column
                        mag_step.append(tot_mag)
                    except ValueError:
                        pass
                i += 1
            
            if len(mag_step) == n_ions:
                magnetization_all_steps.append(mag_step)
        else:
            i += 1
    
    return np.array(magnetization_all_steps)

# Read magnetization data (fast method)
#outcar_path = "/data/hjlee/d_LIRICH/V_void_formation/aimd_calculation/3_300_1000/OUTCAR"
#print("Reading magnetization from OUTCAR...")
#magnetization = read_magnetization_from_outcar(outcar_path, n_ions=144)
#print(f"Magnetization data shape: {magnetization.shape}")
#print(f"Number of ionic steps: {magnetization.shape[0]}")
#print(f"Number of ions: {magnetization.shape[1]}")
