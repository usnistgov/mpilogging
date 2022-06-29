import logging
from mpi4py import MPI

class MPIRankFilter(logging.Filter):
    """
    A filter class that injects information about MPI processes.

    Adds additional context of `mpirank` and `mpisize` to logging records.
    """
    def __init__(self, name='', comm=MPI.COMM_WORLD):
        """Initialize filter.

        Parameters
        ----------
        name : str
            The name of the logger which, together with its children, will
            have its events allowed through the filter.  If no name is
            specified, allow every event.
        comm : MPI.Comm
            MPI communicator to add context about.
        """
        self.comm = comm
        super().__init__(name)
    
    def filter(self, record):
        record.mpirank = self.comm.rank
        record.mpisize = self.comm.size

        return True
