import logging
from mpi4py import MPI

class MPIGatheredFileHandler(logging.FileHandler):
    """
    A handler class which gathers formatted logging records from all MPI ranks
    and writes them to a disk file on a single rank.
    """

    def __init__(self, filename, *args, write_rank=0, **kwargs):
        """Open the specified file and use it as the stream for logging.

        Warnings
        --------

        This `~logging.Handler` is prone to deadlocks if an event is not
        logged by all ranks, e.g., if it is made within a conditional that
        not all ranks branch into.  If this is a concern, consider using
        `~.mpiScatteredFileHandler.MPIScatteredFileHandler` instead.

        Parameters
        ----------
        filename : str
            The name of the file to open for logging.
        write_rank : int
            MPI rank that actually writes to the file (default: 0).
        *args
            Arguments are as described in the docstring of
            `~logging.FileHandler`.
        **kwargs
            Keyword arguments are as described in the docstring of
            `~logging.FileHandler`.
        """
        self.write_rank = write_rank
        super().__init__(filename, **kwargs)

    def emit(self, record):
        comm = MPI.COMM_WORLD
        records = comm.gather(record, root=self.write_rank)
        if comm.rank == self.write_rank:
            for rec in records:
                super().emit(rec)
