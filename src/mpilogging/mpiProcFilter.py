import logging
from mpi4py import MPI

class MPIProcFilter(logging.Filter):
    """This filter injects information about MPI processes.
    """
    
    def filter(self, record):
        record.mpirank = MPI.COMM_WORLD.rank
        record.mpisize = MPI.COMM_WORLD.size

        return True
