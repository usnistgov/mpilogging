import logging
from mpi4py import MPI

class MPIScatteredFileHandler(logging.FileHandler):
    def __init__(self, filepattern, *args, **kwargs):
        filename = filepattern % {
            'mpirank': MPI.COMM_WORLD.rank,
            'mpisize': MPI.COMM_WORLD.size
        }
        super().__init__(filename, *args, **kwargs)
