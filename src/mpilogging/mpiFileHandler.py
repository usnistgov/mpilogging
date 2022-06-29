import logging
from mpi4py import MPI

class MPIFileHandler(logging.FileHandler):
    """
    A base handler class which is aware of MPI ranks.
    """

    def __init__(self, filename, *args, comm=MPI.COMM_WORLD, **kwargs):
        """Open the specified file and use it as the stream for logging.

        Parameters
        ----------
        filename : str
            The name of the file to open for logging.
        *args
            Arguments are as described in the docstring of
            `~logging.FileHandler`.
        comm : MPI.Comm
            MPI communicator to gather log records over.
        **kwargs
            Keyword arguments are as described in the docstring of
            `~logging.FileHandler`.
        """
        self.comm = comm
        super().__init__(filename, *args, **kwargs)
