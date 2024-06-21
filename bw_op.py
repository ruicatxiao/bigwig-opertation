import os
import subprocess
from math import log  # Add this line to import the log function

# Define source and output directories
source = "input_bw"
output = "output_bw"

# Function to run a command and handle errors
def run_command(command):
    try:
        subprocess.run(command, check=True)
        print(f"{command} executed successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to execute: {command}")
        return False
    return True

# Process each file in the source directory
for forward in [f for f in os.listdir(source) if f.endswith('_FWD.bw')]:
    fname = forward[:-3]  # Remove extension
    reverse = forward.replace('_FWD.bw', '_REV.bw')
    
    rname = reverse[:-3]
    print(f"Now beginning the following sample: {fname}\t{rname}")
    
    # Temporary files for processing
    tmp_fwd_bg = f"{fname}.temp.bg"
    tmp_rev_bg = f"{rname}.temp.bg"
    
    # Converting BigWig to BedGraph
    if not run_command(["./bigWigToBedGraph", os.path.join(source, forward), tmp_fwd_bg]):
        continue
    if not run_command(["./bigWigToBedGraph", os.path.join(source, reverse), tmp_rev_bg]):
        continue

    # Process with awk and remove temporary files
    with open(tmp_fwd_bg, 'r') as f, open(f"{fname}.4COMPUTE_FWD.bg", 'w') as out:
        for line in f:
            parts = line.strip().split()
            parts[3] = str(log(float(parts[3]) + 1) / log(2))
            out.write("\t".join(parts) + "\n")
    os.remove(tmp_fwd_bg)

    with open(tmp_rev_bg, 'r') as f, open(f"{rname}.4COMPUTE_REV.bg", 'w') as out:
        for line in f:
            parts = line.strip().split()
            parts[3] = str(log(float(parts[3]) + 1) / log(2))
            out.write("\t".join(parts) + "\n")
    os.remove(tmp_rev_bg)

    # Converting BedGraph back to BigWig
    run_command(["./bedGraphToBigWig", f"{fname}.4COMPUTE_FWD.bg", "chrm.sizes", f"{fname}_4COMPUTE_FWD.bw"])
    os.remove(f"{fname}.4COMPUTE_FWD.bg")
    run_command(["./bedGraphToBigWig", f"{rname}.4COMPUTE_REV.bg", "chrm.sizes", f"{rname}_4COMPUTE_REV.bw"])
    os.remove(f"{rname}.4COMPUTE_REV.bg")

    print(f"Finished sample: {fname}\t{rname}")

# Move all output files to the output directory
for file in os.listdir("."):
    if file.endswith("_4COMPUTE_FWD.bw") or file.endswith("_4COMPUTE_REV.bw"):
        os.rename(file, os.path.join(output, file))
