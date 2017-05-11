# Cooperative Yielding Example

This project serves as an example of how eventlet greenthreads can work either
cooperatively or blocking.

```
$ make shell
>>> # Make both calls asynchronously to prevent needing to open up a new shell
>>> n.rpc.primes.cooperative.call_async(10**7, 10**7 + 100)
>>> n.rpc.primes.blocking.call_async(10**7, 10**7 + 100)
```

Then looking at the logs should give you something like:

```bash
$ docker-compose logs runner
runner_1  | Starting cooperative calc
runner_1  | Cooperatively yielding
...
runner_1  | Cooperatively yielding
runner_1  | Starting blocking calc
runner_1  | Completed blocking calc
runner_1  | Cooperatively yielding
runner_1  | <Rpc [primes.blocking] at 0x7f474c596208>: Found 2 primes between 10000000 and 10000100 in 1.9453198310002335 seconds
runner_1  | Cooperatively yielding
...
runner_1  | Cooperatively yielding
runner_1  | completed cooperative calc
runner_1  | <Rpc [primes.cooperative] at 0x7f474c596780>: Found 2 primes between 10000000 and 10000100 in 4.02776659600022 seconds
```

To decrypt the logs a little:

```bash
$ docker-compose logs runner
runner_1  | Starting cooperative calc
# cooperative loop starts
runner_1  | Cooperatively yielding
...
# cooperative loop continues
runner_1  | Cooperatively yielding
# blocking thread starts
runner_1  | Starting blocking calc
# blocking thread completes
runner_1  | Completed blocking calc
# cooperative loop picks back up due to I/O writing to stdout
runner_1  | Cooperatively yielding
# blocking thread prints log after previous loop is complete
runner_1  | <Rpc [primes.blocking] at 0x7f474c596208>: Found 2 primes between 10000000 and 10000100 in 1.9453198310002335 seconds
# cooperative loop continues
runner_1  | Cooperatively yielding
...
runner_1  | Cooperatively yielding
# cooperative loop completes
runner_1  | completed cooperative calc
# cooperative loop logs to stdout
runner_1  | <Rpc [primes.cooperative] at 0x7f474c596780>: Found 2 primes between 10000000 and 10000100 in 4.02776659600022 seconds
```

