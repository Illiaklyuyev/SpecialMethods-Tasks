from mpi4py import MPI
import numpy as np

N = 100

comm=MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()

if rank == 0:
    send_array = np.linspace(1, N, num=N, dtype=np.float64)
else:
    send_array = None

recv_array = np.empty(int(N/size), dtype = np.float64)
comm.Scatter(
    [send_array, MPI.DOUBLE],
    [recv_array, MPI.DOUBLE],
)
print(f"rank {rank}: {recv_array = }")

comm.barrier()

array_sum = recv_array.sum()
print(f"rank {rank}: {array_sum = }")

comm.barrier()

send_array = np.array([array_sum], dtype=np.float64)
print(f'Gathering {send_array} from {rank}.', flush = True)

if rank == 0:
    recv_array = np.empty(size, dtype=np.float64)
else:
    recv_array = None

comm.Gather(
    [send_array, MPI.DOUBLE],
    [recv_array, MPI.DOUBLE],
)

comm.barrier()

if rank == 0:
    print(f"{recv_array = }")
    recv_array_sum = recv_array.sum()
    print(f"{recv_array_sum = }")

