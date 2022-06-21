import logging
from mpi4py import MPI

class MPIProcFilter(logging.Filter):
    """
    A filter class that injects information about MPI processes.

    Adds additional context of `mpirank` and `mpisize` to logging records.
    """
    
    def filter(self, record):
        record.mpirank = MPI.COMM_WORLD.rank
        record.mpisize = MPI.COMM_WORLD.size

        return True
