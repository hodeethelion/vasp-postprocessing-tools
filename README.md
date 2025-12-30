# VASP Post-Processing Tools

A collection of Python tools for post-processing VASP calculation output files.

## Requirements

- Python 3.x
- pymatgen
- numpy
- matplotlib
- tqdm

Install dependencies:
```bash
pip install pymatgen numpy matplotlib tqdm
```

## Tools

### 1. `aimd_magnetization_steps.py`

Extract magnetization data from AIMD (Ab Initio Molecular Dynamics) OUTCAR files.

**Features:**
- Fast parsing of magnetization (x) data from OUTCAR
- Extracts 'tot' column for all ions across all ionic steps
- Returns data as numpy array with shape `(n_ionic_steps, n_ions)`

**Usage:**
```python
from aimd_magnetization_steps import read_magnetization_from_outcar

# Read magnetization data
magnetization = read_magnetization_from_outcar("OUTCAR", n_ions=144)

print(f"Shape: {magnetization.shape}")
print(f"Ionic steps: {magnetization.shape[0]}")
print(f"Number of ions: {magnetization.shape[1]}")
```

---

### 2. `Li_each_delithiation.py`

Generate Li vacancy structures by systematically removing one Li atom at a time. Useful for studying delithiation processes in battery materials.

**Features:**
- Automatically identifies all Li atoms in a structure
- Creates separate POSCAR files for each Li vacancy configuration
- Command-line interface for easy usage

**Usage:**
```bash
# Basic usage (reads POSCAR, outputs to Li_vacancy_structures/)
python Li_each_delithiation.py

# Custom input/output
python Li_each_delithiation.py -i CONTCAR -o vacancy_structures

# Show help
python Li_each_delithiation.py --help
```

**Arguments:**
| Argument | Description | Default |
|----------|-------------|---------|
| `-i`, `--input` | Input structure file | `POSCAR` |
| `-o`, `--output` | Output directory | `Li_vacancy_structures` |

---

### 3. `partial_occupancy.py`

Interactive tool for generating ordered structures from disordered/partial occupancy structures using pymatgen's enumeration algorithms.

**Features:**
- Load any structure file (POSCAR, CIF, etc.)
- Display lattice parameters (a, b, c) and atom counts
- Optional supercell creation
- Define substitution transformations interactively
- Generate enumerated ordered structures with configurable algorithms
- Optional duplicate filtering with symmetry precision control
- Save in VASP (POSCAR) or CIF format

**Usage:**
```bash
python partial_occupancy.py
```

**Interactive Workflow:**
1. Enter structure file path
2. Optionally create supercell (e.g., `2 2 2`)
3. Define substitutions for each element (e.g., `Li+:13,Ti4+:13`)
4. Set extend_collection number (max structures to generate)
5. Optionally apply duplicate filter
6. Save structures to output directory

**Example Session:**
```
Enter structure file path: ./MgO.vasp

✓ Structure loaded: ./MgO.vasp
  Formula: MgO
  Number of atoms: 8
  Lattice: a=4.2112 Å, b=4.2112 Å, c=4.2112 Å

Do you want to make a supercell? (y/n): y
Enter supercell dimensions: 2 2 2

Element: Mg (32 sites)
  Substitutions for Mg: Li+:13,Ti4+:13

Element: O (32 sites)
  Substitutions for O: O2-:32

Enter extend_collection number: 200
Apply RemoveDuplicatesFilter? (y/n): y
Enter output directory: ./gen_str
Enter filename prefix: li13ti13o32
```

---

## License

MIT License

## Author
Copyright (c) 2024 Hodee

Permission is hereby granted, free of charge, to any person obtaining a copy...