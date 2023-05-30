from mpi4py import MPI
import numpy as np

N = 3

A = np.array([
    [43, 1, 2],
    [9, 31, 0],
    [8, 4, 50],
])

B = np.array([
    6,
    5,
    7,
])

ITERATION_MAX = 1000

comm=MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()

x_array = np.zeros(N)
for i in range(ITERATION_MAX):
    print(f"rank {rank}: {x_array = }")
    x_new = (
        B[rank]
        -
        sum(
            map(
                lambda k: A[rank, k]*x_array[k],
                filter(
                    lambda k: k != rank,
                    list(range(0, N))
                )
            )
        )
    ) / A[rank][rank]
    x_array[rank] = x_new

    for j in range(N):
        comm.send(
            x_array[rank],
            dest=j
        )
        x_array[j] = comm.recv(source=j)

    comm.barrier()
    if rank == 0:
        print()
    comm.barrier()

