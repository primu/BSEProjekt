from mpi4py import MPI


class MPIWrapper(object):

    _comm = None
    _rank = None
    _size = None

    _main_node_id = None
    _worker_nodes_ids = None

    def __init__(self):
        self._comm = MPI.COMM_WORLD
        self._rank = self._comm.Get_rank()
        self._size = self._comm.Get_size()
        self._main_node_id = 0
        self._worker_nodes_ids = range(1, self._size)

    def run(self):
        if self.is_main_node():
            self.main_node_task()
        else:
            self.worker_node_task()

    def stop(self):
        raise NotImplementedError("stop is not implemented")

    def is_main_node(self):
        return self._rank == 0

    def is_worker_node(self):
        return self._rank > 0

    def main_node_task(self):
        raise NotImplementedError("main_node_task not implemented")

    def worker_node_task(self):
        raise NotImplementedError("worker_node_task not implemented")

