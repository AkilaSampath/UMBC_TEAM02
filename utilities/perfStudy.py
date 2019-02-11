import subprocess as sub
import sys

"""
To run normally, replacing directories and *not* submitting jobs, type
python makeDirs.py TODO Which file will be run?

To remove the directories
python makeDirs.py -r

To submit jobs,
python makeDirs.py -s

To specify which file should be run, use
-f program_name

The submit tag is "recessive", in the sense that other tags will overwrite it. It also
mandates using the singleton option for the script.
"""

#Non command line arguments
nVals    = [1, 2, 4, 8, 16]
ppnVals  = [1, 2, 4, 6, 8, 16]
arg1Vals = [19]
arg2Vals = ["xx", "sine"]

runNum = len(nVals)*len(ppnVals)*len(arg1Vals)*len(arg2Vals)

#Command line arguments
submit = False
remove = False
program_name = "poisson"

args = sys.argv[1:]
while(len(args) > 0):
    if(args[0] == "-s" and not remove):
        print "Submitting jobs this run:"
        submit = True
    elif(args[0] == "-r"):
        print "Removing folders this run:"
        remove = True
        submit = False
    elif(args[0] == "-f"):
        if(len(args) > 1):
            program_name = args[1]
            args = args[1:]
        else:
            print("No argument after -f")
            exit()
    args = args[1:]

#Double check if submitting
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
        for arg1 in arg1Vals:
            for arg2 in arg2Vals:

                #Create directory name
                dirName = "".join([str(s) for s in ["n", n, "ppn", ppn, "a", arg1, "b", arg2]])

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
                    outfile = open("/".join([dirName, program_name + ".slurm"]),"w")

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
                        outfile.write("srun ./" + program_name + " " + arg1 + " "+ arg2 + "\n")
                        outfile.close()

                        sub.call(["sbatch", "/".join([dirName,program_name + ".slurm"])])

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
                        outfile.write("srun ../" + " ".join([str(s) for s in [program_name, arg1, arg2]]) + "\n")
                        outfile.close()
