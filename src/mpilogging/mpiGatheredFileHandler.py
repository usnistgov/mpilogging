import logging
from mpi4py import MPI

class MPIGatheredFileHandler(logging.FileHandler):
    """
    A handler class which gathers formatted logging records from all MPI ranks
    and writes them to a disk file on a single rank.
    """

    def __init__(self, filename, **kwargs):
        """Open the specified file and use it as the stream for logging.

        Warnings
        --------

        This `~logging.Handler` is prone to deadlocks if all ranks do not
        log at the same time.  If this is a concern, consider using
        `~.mpiScatteredFileHandler.MPIScatteredFileHandler` instead.

        Parameters
        ----------
        filename : str
            The name of the file to open for logging.
        **kwargs
            Keyword arguments are as described in the docstring of
            `~logging.FileHandler`.
        """
        super().__init__(filename, **kwargs)

    def emit(self, record):
        comm = MPI.COMM_WORLD
        records = comm.gather(record, root=0)
        if comm.rank == 0:
            for record in records:
                super().emit(record)
