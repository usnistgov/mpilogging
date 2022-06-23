# MPI Logging

This package provides a [logging
filter](https://docs.python.org/3/library/logging.html#filter-objects) that
adds context about MPI processes and [logging
handlers](https://docs.python.org/3/library/logging.html#handler-objects)
that are MPI-aware.

## Installation

```shell
$ pip install mpilogging
```

## Usage

### Separate log files for each rank

The simplest way to log from multiple MPI ranks is with a
`MPIScatteredFileHandler`,

```python
import logging
import logging.config

config = {
    "version": 1,
    "handlers": {
        "scatterfile": {
            "class": "mpilogging.MPIScatteredFileHandler",
            "filepattern": "mpilogging.%(mpirank)d_of_%(mpisize)d.log"
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
```

If this script is invoked with `mpirun -np 3`, then three files will be
created in the local working directory, one for each rank,

```
mpilogging.0_of_3.log
mpilogging.1_of_3.log
mpilogging.2_of_3.log
```

each of which will record the message logged by the respective rank.

### Merged log file for all ranks

An `MPIGatheredFileHandler` may be used if it is desired to collect all log
messages from all ranks in a single file.  In this case, it is advisable to
use an `MPIRankFilter` to add context to each log message,

```
import logging
import logging.config

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
            "filename": "mpilogging.log"
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
```

If invoked with `mpirun -np 3`, this would result in a single log file
`mpilogging.log`, containing

```
0 of 3 : DEBUG : a debug message
1 of 3 : DEBUG : a debug message
2 of 3 : DEBUG : a debug message
0 of 3 : INFO : an info message
1 of 3 : INFO : an info message
2 of 3 : INFO : an info message
```

**Warning:** Be aware that the `MPIGatheredFileHandler` will deadlock if
all ranks do not log at the same time.  If this is a concern, then
`MPIScatteredFileHandler` is recommended.

## Testing

```shell
$ pytest
```

or

```shell
$ mpirun -np <#ranks> pytest
```
