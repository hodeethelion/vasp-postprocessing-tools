from pymatgen.core import Structure
import os
import argparse


def main():
    # Set up argument parser for user-friendly input
    parser = argparse.ArgumentParser(
        description='Generate Li vacancy structures by removing one Li atom at a time.'
    )
    parser.add_argument(
        '-i', '--input',
        type=str,
        default='POSCAR',
        help='Input structure file (default: POSCAR)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='Li_vacancy_structures',
        help='Output directory for vacancy structures (default: Li_vacancy_structures)'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found!")
        return
    
    # Load the pristine structure
    pristine = Structure.from_file(args.input)
    print(f"Loaded structure from: {args.input}")
    
    # Find all Li atoms in the structure
    li_indices = [i for i, site in enumerate(pristine) if site.species_string == 'Li']
    
    if len(li_indices) == 0:
        print("Error: No Li atoms found in the structure!")
        return
    
    print(f"Found {len(li_indices)} Li atoms in the structure")
    
    # Create a directory to store the defect structures
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        print(f"Created output directory: {args.output}")
    
    # Create structures, each with one Li atom removed
    for i, li_index in enumerate(li_indices):
        # Create a copy of the pristine structure
        defect_structure = pristine.copy()
        
        # Remove one Li atom
        defect_structure.remove_sites([li_index])
        
        # Save the defect structure to a POSCAR file
        filename = os.path.join(args.output, f'POSCAR_Li_vacancy_{i+1}')
        defect_structure.to(filename=filename+'.vasp', fmt='poscar')
        
        print(f"Created structure with Li vacancy at site {li_index}, saved as {filename}.vasp")
    
    print(f"\nDone! Generated {len(li_indices)} structures with Li vacancies in '{args.output}/'")


if __name__ == '__main__':
    main()
