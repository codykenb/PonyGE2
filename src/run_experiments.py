""" This program cues up and executes multiple runs of PYGE. Results of runs
    are parsed and placed in a spreadsheet for easy visual analysis.

    Copyright (c) 2014 Michael Fenton
    Hereby licensed under the GNU GPL v3."""

from utilities.algorithm.initialise_run import check_python_version

check_python_version()

from multiprocessing import cpu_count, Pool
from operator import itemgetter
from datetime import datetime
from subprocess import call
from os.path import join

from stats.parse_stats import parse_stat_from_runs


def execute_run(run, experiment_name):
    """
    Initialise all aspects of a run.
    
    :return: Nothing.
    """

    cmd = "python ponyge.py --silent --parameters regex_match.txt " \
          "--target '\d.[9-n](\d.).(\w.).(\w.).(\d.).\w\d|([" \
          "0-9a-fA-F]:?){12}' --experiment_name " + experiment_name + \
          " --random_seed " + str(run)

    call(cmd, shell=True)


def execute_runs(cores, runs, experiment_name):
    """ Execute multiple runs in series using multiple cores to evaluate each
        population. """

    results, run_results = [], []
    time1 = datetime.now()
    pool = Pool(processes=cores)
    
    print("\nMulti-Run Start:", time1, "\n")

    for run in range(runs):

        # Execute a single evolutionary run.
        results.append(pool.apply_async(execute_run, (run, experiment_name)))
    
    for result in results:
        result.get()
    
    pool.close()
    
    # Save spreadsheet and average fitness plot for runs so far.
    parse_stat_from_runs(experiment_name, ["best_fitness"], True)

    time2 = datetime.now()
    total_time = time2 - time1

    # Write info about best indiv from each run to a file.
    filename = join("..", "results", experiment_name, experiment_name + ".txt")
    savefile = open(filename, 'w')
    for ans, answer in enumerate(run_results):
        savefile.write("Run " + str(ans) + "\tName: " + str(answer[0]) +
                       "\tBest: " + str(answer[1]) + "\n")
    run_results.sort(key=itemgetter(1))

    # Write info about best overall result.
    savefile.write("\nBEST: " + str(run_results[-1]))
    savefile.write("\n\nTotal time taken for " + str(runs) +
                   " runs: " + str(total_time))
    savefile.close()

    print("\nTotal time taken for", runs, "runs:", total_time)
    print("\nBEST:", run_results[-1])


if __name__ == "__main__":
    # Setup run parameters.
    runs = 30
    cores = cpu_count() - 1

    # Execute multiple runs.
    execute_runs(cores, runs, "REGEX")
