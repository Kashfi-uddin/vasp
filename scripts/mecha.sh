#!/bin/bash

# Prompt user for the number of top-level folders and their names
read -p "Enter the number of top-level folders: " num_folders

declare -a folder_names
for ((i=1; i<=num_folders; i++)); do
    read -p "Enter the name of top-level folder $i: " folder_name
    folder_names+=("$folder_name")
done

# Iterate over each top-level folder
for top_folder in "${folder_names[@]}"; do
    if [ -d "$top_folder" ]; then
        echo "Entering top-level folder: $top_folder"
        cd "$top_folder"

        # Iterate over each sub-folder inside the top-level folder
        for sub_folder in */; do
            if [ -d "$sub_folder" ]; then
                echo "  Entering sub-folder: $sub_folder"
                cd "$sub_folder"

                # Run VASP in the sub-folder
                if [ -f "POSCAR" ]; then
                    echo "    Running VASP in $(pwd)"
                    mpirun -np 32 vasp_std | tee vasp.out
                else
                    echo "    Skipping: POSCAR not found in $(pwd)"
                fi

                cd .. # Return to the top-level folder
            fi
        done

        cd .. # Return to the main directory
    else
        echo "Top-level folder $top_folder does not exist!"
    fi

done

echo "All calculations are complete!"

