"""Execute the COMPAS notebook using this exact Python environment as kernel."""
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

base = Path(__file__).resolve().parent
path = base / 'COMPAS_reconciliado.ipynb'
notebook = nbformat.read(path, as_version=4)
nbformat.validate(notebook)
manager = KernelManager(kernel_name='python3')
# In-memory override only; do not install or modify a machine-wide kernelspec.
manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
try:
    NotebookClient(notebook, km=manager, timeout=180, resources={'metadata': {'path': str(base)}}).execute()
finally:
    if manager.has_kernel:
        manager.shutdown_kernel(now=True)
nbformat.validate(notebook)
errors = [o for c in notebook.cells if c.cell_type == 'code' for o in c.outputs if o.output_type == 'error']
assert not errors
nbformat.write(notebook, path)
print(f'Executed and validated: {path}')
