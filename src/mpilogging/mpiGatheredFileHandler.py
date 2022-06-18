import logging
from mpi4py import MPI
import sys

class MPIGatheredFileHandler(logging.FileHandler):

    def emit(self, record):
        comm = MPI.COMM_WORLD
        records = comm.gather(record, root=0)
        if comm.rank == 0:
            for record in records:
                super().emit(record)
