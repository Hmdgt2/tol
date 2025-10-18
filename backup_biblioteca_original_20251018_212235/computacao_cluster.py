# lib/funcoes_analiticas/computacao_cluster.py
try:
    from mpi4py import MPI
    MPI_AVAILABLE = True
except ImportError:
    MPI_AVAILABLE = False
from typing import List, Dict
import numpy as np

def mpi_distributed_analysis(seq: List[float]) -> Dict:
    """Análise distribuída usando MPI para clusters."""
    if not MPI_AVAILABLE:
        return {'mpi_analysis': 'mpi4py_not_available'}
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Divide a sequência entre processos
    local_size = len(seq) // size
    local_seq = seq[rank * local_size: (rank + 1) * local_size]
    
    # Processamento local
    local_mean = np.mean(local_seq)
    local_fft = np.fft.fft(local_seq)
    
    # Coleta resultados
    all_means = comm.gather(local_mean, root=0)
    all_fft = comm.gather(local_fft, root=0)
    
    if rank == 0:
        global_mean = np.mean(all_means)
        global_fft = np.concatenate(all_fft)
        
        return {
            'distributed_computation': {
                'global_mean': float(global_mean),
                'fft_size': len(global_fft),
                'process_count': size,
                'efficiency': len(seq) / (local_size * size)
            },
            'mpi_implementation': 'full_distributed'
        }
    else:
        return {'mpi_analysis': f'process_{rank}_completed'}
