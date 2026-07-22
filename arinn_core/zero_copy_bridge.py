import os
import uuid
import numpy as np # type: ignore

try:
    import pyarrow as pa # type: ignore
    import pyarrow.ipc as ipc # type: ignore
except ImportError:
    pa = None

class MemoryBridge:
    """
    Vaults 3 & 17 Implementation: The Zero-Copy Memory Bridge
    Allocates Arrow buffers via Memory-Mapped files for pure Zero-Copy IPC.
    This enables highly-optimized binaries (e.g., dynamically compiled Rust kernels)
    to read ARINN's internal tensor state instantly without serialization overhead.
    """
    def __init__(self, base_dir="data/ipc_bridges"):
        if not pa:
            raise ImportError("PyArrow is required for the Zero-Copy Memory Bridge.")
            
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.mmap_path = os.path.join(self.base_dir, f"bridge_{uuid.uuid4().hex}.arrow")
        
    def write_tensor(self, tensor_data: np.ndarray) -> str:
        """
        Writes a numpy array to the memory-mapped file via Arrow.
        Returns the file path that the MSVC Rust/C++ kernel can memory-map directly.
        """
        # Convert numpy to Arrow Array and Batch
        arrow_array = pa.array(tensor_data) # type: ignore
        batch = pa.RecordBatch.from_arrays([arrow_array], names=['tensor']) # type: ignore
        
        # Write format strictly to OS-level Memory Map file
        with pa.OSFile(self.mmap_path, 'wb') as sink: # type: ignore
            with ipc.new_file(sink, batch.schema) as writer:
                writer.write_batch(batch)
                
        return self.mmap_path
        
    def read_tensor(self) -> np.ndarray:
        """
        Reads the shared memory back into a numpy array (zero-copy view).
        The data memory is directly backed by the OS file without copying to Python space.
        """
        with pa.memory_map(self.mmap_path, 'r') as source: # type: ignore
            reader = ipc.RecordBatchFileReader(source)
            batch = reader.get_batch(0)
            return batch.column(0).to_numpy()
            
    def cleanup(self):
        """
        Releases the physical file bridge.
        """
        if os.path.exists(self.mmap_path):
            try:
                os.remove(self.mmap_path)
            except OSError:
                pass
