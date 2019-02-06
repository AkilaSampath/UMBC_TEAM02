import subprocess as sub
import sys

"""
To run normally, type
python makeDirs.py

To remove the nodes
python makeDirs.py -r
"""

nVals    = [1, 2, 4, 8, 16, 20]
ppnVals  = [1, 2, 4, 6, 8, 16]
trapPows = [19]
trapVals = [2**t for t in trapPows] #Unused

for n in nVals:
    for ppn in ppnVals:
        for trap in trapPows:
            dirName = "".join([str(s) for s in ["n", n, "ppn", ppn, "tr", trap ]])
            #Make Directory
            sub.call(["rm", "-rf", dirName])
            if(len(sys.argv) > 1):
                if(sys.argv[1] == "-r"):
                    print "Removed", dirName
            else:
                sub.call(["mkdir", dirName])
                
                #Write slurm file
                outfile = open("/".join([dirName, "trap.slurm"]),"w")

                outfile.write("#!/bin/bash\n")
                outfile.write("#SBATCH --job-name=Team2_Trap\n")
                outfile.write("#SBATCH --output=slurm.out\n")
                outfile.write("#SBATCH --error=slurm.err\n")
                outfile.write("# The develop partition always goes with the normal qos\n")
                outfile.write("#SBATCH --partition=batch\n")
                outfile.write("#SBATCH --qos=short\n")
                outfile.write("#SBATCH --nodes=" + str(n) + "\n")
                outfile.write("#SBATCH --ntasks-per-node=" + str(ppn) + "\n")
                outfile.write("#SBATCH --constraint=hpcf2013" + "\n")
                outfile.write("\n")
                outfile.write("srun ../trap 0.0 1.0 " + str(2**trap) + "\n")

                outfile.close()
