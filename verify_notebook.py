"""Execute the notebook in a fresh kernel and save verified outputs."""
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parent
path = root / 'Flight_Analysis' / 'Flights.ipynb'
nb = nbformat.read(path, as_version=4)
km = KernelManager(kernel_name='python3')
km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
try:
    NotebookClient(nb, km=km, timeout=180, resources={'metadata': {'path': str(path.parent)}}).execute()
finally:
    if km.has_kernel:
        km.shutdown_kernel(now=True)
nbformat.validate(nb)
assert all(o.output_type != 'error' for c in nb.cells if c.cell_type == 'code' for o in c.outputs)
nbformat.write(nb, path)
for c in nb.cells:
    if c.cell_type == 'code':
        for o in c.outputs:
            if o.output_type == 'stream':
                print(o.text)
            elif 'text/plain' in o.get('data', {}) and 'image/png' not in o.data:
                print(o.data['text/plain'])
print('Fresh-kernel execution passed and outputs saved.')
