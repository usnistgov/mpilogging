import logging
from mpi4py import MPI

from mpilogging import MPIScatteredFileHandler, MPIGatheredFileHandler, MPIRankFilter

def test_scattered_logging(mpi_tmpdir):
    """Test that log messages are recorded in a separate file by rank
    """

    # mpi_tmpdir is a pathlib.Path
    filepattern = str(mpi_tmpdir / "mpi.rank%(mpirank)d.log")

    log = logging.getLogger("mpilogging")

    handler = MPIScatteredFileHandler(filepattern=filepattern)
    formatter = logging.Formatter("%(levelname)s : %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    log.debug("a debug message")
    log.info("an info message")
    
    filename = filepattern % {
        'mpirank': MPI.COMM_WORLD.rank,
        'mpisize': MPI.COMM_WORLD.size
    }

    with open(filename, mode='r') as fd:
        txt = fd.read()

    expect = ["DEBUG : a debug message", "INFO : an info message"]

    assert txt.strip() == "\n".join(expect)


def test_gathered_logging(mpi_tmpdir):
    """Test that log messages are recorded in a single file for all ranks
    """

    # mpi_tmpdir is a pathlib.Path
    filename = str(mpi_tmpdir / "mpi.log")
    log = logging.getLogger("mpilogging")
    
    handler = MPIGatheredFileHandler(filename=filename)
    mpifilter = MPIRankFilter()
    handler.addFilter(mpifilter)
    formatter = logging.Formatter("%(mpirank)d of %(mpisize)d : %(levelname)s : %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    log.setLevel(logging.DEBUG)

    log.debug("a debug message")
    log.info("an info message")
    
    MPI.COMM_WORLD.Barrier()
    
    with open(filename, mode='r') as fd:
        txt = fd.read()

    expect = []
    for rank in range(MPI.COMM_WORLD.size):
        expect.append("%(mpirank)d of %(mpisize)d : DEBUG : a debug message" % {
                          "mpirank": rank,
                          "mpisize": MPI.COMM_WORLD.size
                      })
    for rank in range(MPI.COMM_WORLD.size):
        expect.append("%(mpirank)d of %(mpisize)d : INFO : an info message" % {
                          "mpirank": rank,
                          "mpisize": MPI.COMM_WORLD.size
                      })

    assert txt.strip() == "\n".join(expect)    
