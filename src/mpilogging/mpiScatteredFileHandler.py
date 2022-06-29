from mpi4py import MPI

from .mpiFileHandler import MPIFileHandler


class MPIScatteredFileHandler(MPIFileHandler):
    """
    A handler class which writes formatted logging records to distinct disk
    files for each MPI rank.
    """

    def __init__(self, filepattern, *args, comm=MPI.COMM_WORLD, **kwargs):
        """Open the specified file and use it as the stream for logging.

        Parameters
        ----------
        filepattern : str
            A %-formatted pattern for the creation of filenames, which
            allows for the substitutions `'%(mpirank)s'` and
            `'%(mpisize)s'` to create unique filenames on each rank.  If
            the filename on each MPI rank is not unique, the results are
            not predictable and the redundant file may be corrupted.
        *args
            Arguments are as described in the docstring of
            `~logging.FileHandler`.
        comm : MPI.Comm
            MPI communicator to scatter log records over.
        **kwargs
            Keyword arguments are as described in the docstring of
            `~logging.FileHandler`.
        """
        if 'filename' in kwargs:
            raise TypeError("Expected `filepattern`, instead of `filename`")

        filename = filepattern % {
            'mpirank': comm.rank,
            'mpisize': comm.size
        }
        super().__init__(filename, *args, comm=comm, **kwargs)
