import eventlet
import logging
import time
import weakref
from nameko.extensions import DependencyProvider
from nameko.rpc import rpc

_log = logging.getLogger(__name__)


class PrimeChecker(DependencyProvider):

    def is_prime(self, number):
        for i in range(2, number):
            if number % i == 0:
                return False
        return True

    def get_dependency(self, worker_ctx):
        return self.is_prime


class EntrypointLogger(DependencyProvider):

    def setup(self):
        self.entrypoint_starts = weakref.WeakKeyDictionary()

    def worker_setup(self, worker_ctx):
        self.entrypoint_starts[worker_ctx] = time.perf_counter()

    def worker_result(self, worker_ctx, result=None, exc_info=None):
        if not result:
            return

        start_time = self.entrypoint_starts.get(worker_ctx, None)
        if start_time:
            execution_time = time.perf_counter() - start_time
        else:
            execution_time = 'unknown'

        _log.info(
            '{0}: Found {1} primes between {2} and {3} in {4} seconds'.format(
                worker_ctx.entrypoint,
                len(result),
                worker_ctx.args[0],
                worker_ctx.args[1],
                execution_time,
            )
        )


class PrimeService:
    name = "primes"

    is_prime = PrimeChecker()
    entrypoint_logger = EntrypointLogger()

    @rpc
    def blocking(self, start, stop):
        _log.info('Starting blocking calc')
        result = [
            x for x in range(start, stop + 1) if self.is_prime(x)
        ]
        _log.info('Completed blocking calc')
        return result

    @rpc
    def cooperative(self, start, stop):
        _log.info('Starting cooperative calc')
        result = []

        for x in range(start, stop + 1):
            if self.is_prime(x):
                result.append(x)

            # Indicate that eventlet can yeild control to another greenthread.
            # If there is no contention, processing will resume in this thread
            # immediately.
            _log.info('Cooperatively yielding')
            eventlet.sleep()

        _log.info('completed cooperative calc')
        return result
