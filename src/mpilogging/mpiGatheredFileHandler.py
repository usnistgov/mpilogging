from mpi4py import MPI

from .mpiFileHandler import MPIFileHandler

class MPIGatheredFileHandler(MPIFileHandler):
    """
    A handler class which gathers formatted logging records from all MPI ranks
    and writes them to a disk file on a single rank.
    """

    def __init__(self, filename, *args, write_rank=0, comm=MPI.COMM_WORLD, **kwargs):
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
        *args
            Arguments are as described in the docstring of
            `~logging.FileHandler`.
        write_rank : int
            MPI rank that actually writes to the file (default: 0).
        comm : MPI.Comm
            MPI communicator to gather log records over.
        **kwargs
            Keyword arguments are as described in the docstring of
            `~logging.FileHandler`.
        """
        self.write_rank = write_rank
        super().__init__(filename, *args, comm=comm, **kwargs)

    def emit(self, record):
        records = self.comm.gather(record, root=self.write_rank)
        if self.comm.rank == self.write_rank:
            for rec in records:
                super().emit(rec)
