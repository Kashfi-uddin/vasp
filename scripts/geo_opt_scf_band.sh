#!/bin/bash

# Paths to input files
INCAR_GEO_OPT="INCAR_GEO_OPT"
INCAR_SCF_OPT="INCAR_SCF_OPT"
INCAR_BAND="INCAR_BAND"
KPOINTS="KPOINTS"
POSCAR="POSCAR"
POTCAR="POTCAR"

# VASP executable and parallel settings
VASP_EXEC="mpirun -np 36 vasp_std"  # Modify if needed

# Create directories for each step
mkdir -p geo_opt scf band

# Geometry Optimization
echo "Starting geometry optimization..."

# Copy necessary files to geo_opt directory
cp $INCAR_GEO_OPT geo_opt/INCAR
cp $POSCAR geo_opt/POSCAR
cp $POTCAR geo_opt/POTCAR
cp $KPOINTS geo_opt/KPOINTS

# Run VASP in geo_opt with live output
cd geo_opt
$VASP_EXEC | tee geo_opt.log
if [ $? -ne 0 ]; then
    echo "Geometry optimization failed."
    exit 1
fi
echo "Geometry optimization completed."

# Self-Consistent Field (SCF) Optimization
echo "Starting SCF optimization..."

# Copy necessary files to scf directory
cd ..
cp geo_opt/CONTCAR scf/POSCAR
cp $INCAR_SCF_OPT scf/INCAR
cp $POTCAR scf/POTCAR
cp $KPOINTS scf/KPOINTS

# Run VASP in scf directory with live output
cd scf
$VASP_EXEC | tee scf_opt.log
if [ $? -ne 0 ]; then
    echo "SCF optimization failed."
    exit 1
fi
echo "SCF optimization completed."

# Band Structure Calculation
echo "Starting band structure calculation..."

# Copy necessary files to band directory
cd ..
cp scf/CHGCAR band/CHGCAR
cp scf/WAVECAR band/WAVECAR
cp scf/POSCAR band/POSCAR
cp $POTCAR band/POTCAR
cp $INCAR_BAND band/INCAR

# Run Vaspkit to generate KPOINTS from KPATH.in
cd band
vaspkit -task 303 | tee vaspkit_303.log
if [ $? -ne 0 ]; then
    echo "Vaspkit KPATH generation failed."
    exit 1
fi

# Rename KPATH.in to KPOINTS
mv KPATH.in KPOINTS

# Run VASP for band structure calculation with live output
$VASP_EXEC | tee band_calc.log
if [ $? -ne 0 ]; then
    echo "Band structure calculation failed."
    exit 1
fi

# Extract band data using Vaspkit
vaspkit -task 211 | tee vaspkit_211.log
if [ $? -ne 0 ]; then
    echo "Vaspkit band data extraction failed."
    exit 1
fi

echo "Band structure calculation and extraction completed."

# End of the script
echo "All steps completed successfully!"
