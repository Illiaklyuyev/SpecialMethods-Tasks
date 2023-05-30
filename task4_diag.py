from mpi4py import MPI
import numpy as np

N = 4

comm=MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()

matrix = np.random.rand(N, N)
print(f"rank {rank}: {matrix = }")
diag = matrix.diagonal().copy()

comm.Bcast(
    [diag, MPI.DOUBLE],
    root = 0
)

comm.barrier()

print(f"rank {rank}: {diag = }")

for i in range(N):
    matrix[i, i] = diag[i]

comm.barrier()

print(f"rank {rank}: {matrix = }")

