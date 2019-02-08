import subprocess as sub
import sys

"""
To run normally, type
python makeDirs.py

To remove the directories
python makeDirs.py -r
"""

nVals    = [1, 2, 4, 8, 16]
ppnVals  = [1, 2, 4, 6, 8, 16]
trapPows = [19]
trapVals = [2**t for t in trapPows] #Unused

functions = ["xx", "sine"]

runNum = len(nVals)*len(ppnVals)*len(trapPows)*len(functions)

#Some options:
submit = True


remove = False
if(len(sys.argv) > 1):
    if(sys.argv[1] == "-r"):
        print "Removing folders this run:"
        remove = True
        submit = False

if(submit):
    print "About to submit", str(runNum), "jobs to the server. Are you sure?"
    choice = raw_input("y/Y to run:")
    if(not choice in ["y", "Y"]):
        exit()
    print "Here we go!"

#Note, singleton is mandatory if submit is True. (Do not delete "or submit"!)
singleton = False or submit

for n in nVals:
    for ppn in ppnVals:
        for trap in trapPows:
            for function in functions:

                #Create directory name
                dirName = "".join([str(s) for s in ["n", n, "ppn", ppn, "tr", trap, function]])

                #Remove directory
                if(0 == sub.call(["test", "-e", dirName])):
                    sub.call(["rm", "-r", dirName])
                    if(remove):
                        #Do nothing--just report:
                        print "Removed", dirName

                #If desired, remove directories and *don't* make new ones

                if(not remove):
                    #Make Directory
                    sub.call(["mkdir", dirName])
                    
                    #Write slurm file
                    outfile = open("/".join([dirName, "trap.slurm"]),"w")

                    if(submit): #Will be run from *this* folder: ./
                        #Boilerplate
                        outfile.write("#!/bin/bash                                             \n")
                        outfile.write("#SBATCH --job-name=Team2_Trap_n" + str(n) +            "\n")
                        outfile.write("#SBATCH --output=" + dirName + "/slurm.out" +          "\n")
                        outfile.write("#SBATCH --error=" + dirName + "/slurm.err" +           "\n")
                        outfile.write("# The develop partition always goes with the normal qos \n")
                        outfile.write("#SBATCH --partition=batch                               \n")
                        outfile.write("#SBATCH --qos=short                                     \n")

                        #Specific to run
                        outfile.write("#SBATCH --nodes=" + str(n) +                           "\n")
                        outfile.write("#SBATCH --ntasks-per-node=" + str(ppn) +               "\n")
                        outfile.write("#SBATCH --constraint=hpcf2013" +                       "\n")

                        #When Python submits, need dependencies to avoid overload
                        outfile.write("#SBATCH --dependency=singleton" +                     "\n")

                        outfile.write("\n")
                        outfile.write("srun ./trap " + function + " 0.0 1.0 " + str(2**trap) + "\n")
                        outfile.close()

                        sub.call(["sbatch", "/".join([dirName,"trap.slurm"])])

                    else: #Meant to be run from within the folder: ./dirName/
                        #Boilerplate
                        outfile.write("#!/bin/bash                                             \n")
                        outfile.write("#SBATCH --job-name=Team2_Trap_n" + str(n) +            "\n")
                        outfile.write("#SBATCH --output=slurm.out                              \n")
                        outfile.write("#SBATCH --error=slurm.err                               \n")
                        outfile.write("# The develop partition always goes with the normal qos \n")
                        outfile.write("#SBATCH --partition=batch                               \n")
                        outfile.write("#SBATCH --qos=short                                     \n")

                        #Specific to run
                        outfile.write("#SBATCH --nodes=" + str(n) +                           "\n")
                        outfile.write("#SBATCH --ntasks-per-node=" + str(ppn) +               "\n")
                        outfile.write("#SBATCH --constraint=hpcf2013" +                       "\n")
                        if(singleton):
                            outfile.write("#SBATCH --dependency=singleton" +                     "\n")
                        outfile.write("\n")
                        outfile.write("srun ../trap " + function + " 0.0 1.0 " + str(2**trap) + "\n")
                        outfile.close()
