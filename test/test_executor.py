import time

from mapchete import Executor


def _dummy_process(i, sleep=0):
    time.sleep(sleep)
    return i + 1


def test_sequential_executor():
    items = 10
    count = 0
    with Executor(concurrency=None) as executor:
        # process all
        for future in executor.as_completed(_dummy_process, range(items)):
            count += 1
            assert future.result()
        assert items == count

        # abort
        cancelled = False
        for future in executor.as_completed(_dummy_process, range(items)):
            if cancelled:
                raise RuntimeError()
            assert future.result()
            cancelled = True
            executor.cancel()


def test_concurrent_futures_processes_executor():
    items = 10
    with Executor(concurrency="processes") as executor:
        # process all
        count = 0
        for future in executor.as_completed(_dummy_process, range(items)):
            count += 1
            assert future.result()


def test_concurrent_futures_processes_executor_cancel():
    items = 100
    with Executor(concurrency="processes", max_workers=2) as executor:
        # abort
        for future in executor.as_completed(
            _dummy_process, range(items), fkwargs=dict(sleep=2)
        ):
            assert future.result()
            executor.cancel()
            break

        assert any([future.cancelled() for future in executor.futures])


def test_concurrent_futures_threads_executor():
    items = 100
    with Executor(concurrency="threads", max_workers=2) as executor:
        # abort
        for future in executor.as_completed(
            _dummy_process, range(items), fkwargs=dict(sleep=2)
        ):
            assert future.result()
            executor.cancel()
            break

        assert any([future.cancelled() for future in executor.futures])


def test_dask_executor():
    items = 100
    with Executor(concurrency="dask", max_workers=2) as executor:
        # abort
        for future in executor.as_completed(
            _dummy_process, range(items), fkwargs=dict(sleep=2)
        ):
            assert future.result()
            executor.cancel()
            break

        assert any([future.cancelled() for future in executor.futures])
