import logging
import logging.config
from mpi4py import MPI

def test_scattered_logging(mpi_tmpdir):
    """Test that log messages are recorded in a separate file by rank
    """

    # mpi_tmpdir is a pathlib.Path
    filepattern = str(mpi_tmpdir / "mpi.rank%(mpirank)d.log")
    config = {
        "version": 1,
        "formatters": {
            "brief": {
                "format": "%(levelname)s : %(message)s"
            }
        },
        "handlers": {
            "scatterfile": {
                "class": "mpilogging.MPIScatteredFileHandler",
                "formatter": "brief",
                "filepattern": filepattern
            }
        },
        "loggers": {
            "mpilogging": {
                "level": "DEBUG",
                "handlers": ["scatterfile"]
            }
        }
    }

    logging.config.dictConfig(config)

    log = logging.getLogger("mpilogging")
    
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
    config = {
        "version": 1,
        "formatters": {
            "brief": {
                "format": "%(mpirank)d of %(mpisize)d : %(levelname)s : %(message)s"
            }
        },
        "filters": {
            "mpi_filter": {
                "()": "mpilogging.MPIRankFilter"
            }
        },
        "handlers": {
            "gatherfile": {
                "class": "mpilogging.MPIGatheredFileHandler",
                "filters": ["mpi_filter"],
                "formatter": "brief",
                "filename": filename
            }
        },
        "loggers": {
            "mpilogging": {
                "level": "DEBUG",
                "handlers": ["gatherfile"]
            }
        }
    }

    logging.config.dictConfig(config)

    log = logging.getLogger("mpilogging")
    
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
