import os
from pymatgen.core import Structure
from pymatgen.alchemy.transmuters import StandardTransmuter
from pymatgen.transformations.standard_transformations import SubstitutionTransformation
from pymatgen.transformations.standard_transformations import OrderDisorderedStructureTransformation
from pymatgen.io.vasp.inputs import Poscar
from pymatgen.alchemy.filters import RemoveDuplicatesFilter
from pymatgen.core.periodic_table import Element, Specie


def get_structure():
    """Load structure file interactively."""
    print("\n" + "="*60)
    print("  PARTIAL OCCUPANCY STRUCTURE GENERATOR")
    print("="*60)
    
    file_path = input("\nEnter structure file path (e.g., ./temp_str/MgO.vasp): ").strip()
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found!")
        return None
    
    st = Structure.from_file(file_path)
    print(f"\n✓ Structure loaded: {file_path}")
    print(f"  Formula: {st.composition.reduced_formula}")
    print(f"  Number of atoms: {len(st)}")
    print(f"  Lattice: a={st.lattice.a:.4f} Å, b={st.lattice.b:.4f} Å, c={st.lattice.c:.4f} Å")
    print(f"  Elements: {[str(el) for el in st.composition.elements]}")
    
    return st


def make_supercell(st):
    """Optionally make supercell."""
    print("\n" + "-"*60)
    make_super = input("Do you want to make a supercell? (y/n): ").strip().lower()
    
    if make_super == 'y':
        supercell_input = input("Enter supercell dimensions (e.g., 2 2 2 or 2,2,2): ").strip()
        # Parse input - handle both space and comma separated
        supercell_input = supercell_input.replace(',', ' ')
        dims = [int(x) for x in supercell_input.split()]
        
        if len(dims) != 3:
            print("Error: Need exactly 3 dimensions!")
            return st
        
        st = st.make_supercell(dims)
        print(f"\n✓ Supercell created: {dims[0]}x{dims[1]}x{dims[2]}")
        print(f"  New number of atoms: {len(st)}")
        print(f"  New lattice: a={st.lattice.a:.4f} Å, b={st.lattice.b:.4f} Å, c={st.lattice.c:.4f} Å")
    
    return st


def get_substitution_info(st):
    """Get substitution transformation info from user."""
    print("\n" + "-"*60)
    print("SUBSTITUTION TRANSFORMATION SETUP")
    print("-"*60)
    
    elements = [str(el) for el in st.composition.elements]
    print(f"\nElements in structure: {elements}")
    print(f"Total atoms: {len(st)}")
    
    # Show element counts
    for el in st.composition.elements:
        count = st.composition[el]
        print(f"  {el}: {int(count)} atoms")
    
    substitution_dict = {}
    
    print("\n--- Define substitutions for each element ---")
    print("(Press Enter to skip an element)")
    
    for el in elements:
        el_count = int(st.composition[Element(el)])
        print(f"\nElement: {el} ({el_count} sites)")
        
        sub_input = input(f"  Substitutions for {el} (format: 'Li+:13,Ti4+:13' or skip): ").strip()
        
        if sub_input:
            sub_dict = {}
            pairs = sub_input.split(',')
            total_ratio = 0
            
            for pair in pairs:
                pair = pair.strip()
                if ':' in pair:
                    species, count = pair.split(':')
                    species = species.strip()
                    count = int(count.strip())
                    ratio = count / el_count
                    sub_dict[species] = ratio
                    total_ratio += ratio
                    print(f"    → {species}: {count}/{el_count} = {ratio:.4f}")
            
            if total_ratio > 1.0:
                print(f"  Warning: Total ratio {total_ratio:.4f} > 1.0!")
            
            if sub_dict:
                substitution_dict[el] = sub_dict
    
    return substitution_dict


def apply_transformation(st, substitution_dict):
    """Apply substitution transformation."""
    print("\n" + "-"*60)
    print("APPLYING TRANSFORMATIONS")
    print("-"*60)
    
    print("\nSubstitution dictionary:")
    for el, subs in substitution_dict.items():
        print(f"  {el} → {subs}")
    
    trans = SubstitutionTransformation(substitution_dict)
    subs = trans.apply_transformation(st)
    
    print("\n✓ Substitution transformation applied")
    
    return subs


def generate_ordered_structures(subs):
    """Generate ordered structures from disordered structure."""
    print("\n" + "-"*60)
    print("STRUCTURE ENUMERATION")
    print("-"*60)
    
    extend_collection = input("\nEnter extend_collection number (max structures to generate, e.g., 200): ").strip()
    extend_collection = int(extend_collection) if extend_collection else 200
    
    algo = input("Enter algorithm (1 or 2, default=2): ").strip()
    algo = int(algo) if algo else 2
    
    print(f"\nGenerating structures with extend_collection={extend_collection}, algo={algo}...")
    print("This may take a while...")
    
    enum = OrderDisorderedStructureTransformation(algo=algo)
    transmuter = StandardTransmuter.from_structures(
        [subs],
        transformations=[enum],
        extend_collection=extend_collection
    )
    
    print(f"\n✓ Generated {len(transmuter)} structures")
    
    return transmuter


def apply_filter(transmuter):
    """Optionally apply duplicate filter."""
    print("\n" + "-"*60)
    apply_fil = input("Apply RemoveDuplicatesFilter? (y/n): ").strip().lower()
    
    if apply_fil == 'y':
        symprec = input("Enter symmetry precision (default=1e-5): ").strip()
        symprec = float(symprec) if symprec else 1e-5
        
        print(f"\nApplying filter with symprec={symprec}...")
        fil = RemoveDuplicatesFilter(symprec=symprec)
        transmuter.apply_filter(fil)
        print(f"✓ After filtering: {len(transmuter)} unique structures")
    
    return transmuter


def save_structures(transmuter):
    """Save generated structures."""
    print("\n" + "-"*60)
    print("SAVE STRUCTURES")
    print("-"*60)
    
    output_dir = input("\nEnter output directory (e.g., ./gen_str): ").strip()
    
    if not os.path.exists(output_dir):
        create = input(f"Directory '{output_dir}' doesn't exist. Create it? (y/n): ").strip().lower()
        if create == 'y':
            os.makedirs(output_dir)
            print(f"✓ Created directory: {output_dir}")
        else:
            print("Aborting save.")
            return
    
    filename_prefix = input("Enter filename prefix (e.g., 'li13ti13o32'): ").strip()
    if not filename_prefix:
        filename_prefix = "structure"
    
    file_format = input("Enter format (vasp/cif/poscar, default=poscar): ").strip().lower()
    if not file_format:
        file_format = "poscar"
    
    # Determine extension
    ext_map = {'vasp': 'vasp', 'cif': 'cif', 'poscar': 'vasp'}
    ext = ext_map.get(file_format, 'vasp')
    fmt = 'cif' if file_format == 'cif' else 'poscar'
    
    print(f"\nSaving {len(transmuter)} structures...")
    
    for k in range(len(transmuter)):
        st_final = transmuter.transformed_structures[k].final_structure
        filename = f"{output_dir}/{k}_{filename_prefix}.{ext}"
        st_final.to(filename, fmt=fmt)
    
    print(f"\n✓ Saved {len(transmuter)} structures to {output_dir}/")
    print(f"  Files: 0_{filename_prefix}.{ext} to {len(transmuter)-1}_{filename_prefix}.{ext}")


def main():
    """Main interactive workflow."""
    # Step 1: Load structure
    st = get_structure()
    if st is None:
        return
    
    # Step 2: Optionally make supercell
    st = make_supercell(st)
    
    # Show current structure info
    print(f"\nCurrent structure:")
    print(f"  Formula: {st.composition.reduced_formula}")
    print(f"  Total atoms: {len(st)}")
    
    # Step 3: Get substitution info
    substitution_dict = get_substitution_info(st)
    
    if not substitution_dict:
        print("\nNo substitutions defined. Exiting.")
        return
    
    # Step 4: Apply substitution transformation
    subs = apply_transformation(st, substitution_dict)
    
    # Step 5: Generate ordered structures
    transmuter = generate_ordered_structures(subs)
    
    # Step 6: Optionally apply filter
    transmuter = apply_filter(transmuter)
    
    # Step 7: Save structures
    save_structures(transmuter)
    
    print("\n" + "="*60)
    print("  DONE!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
