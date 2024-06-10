"""
    Streamlit App using Modal Serverless Platform
"""

import shlex
import subprocess
from pathlib import Path

import modal

image = modal.Image.debian_slim().pip_install("streamlit", "numpy", "pandas")

app = modal.App(
    name="streamlit-modal-serverless-app", image=image
)

# Mount app.py script (NOTE: Streamlit runs apps as Python scripts)
streamlit_script_local_path = Path(__file__).parent.parent / "app.py"
print('*****************')
print(streamlit_script_local_path)
print('*****************')
streamlit_script_remote_path = Path("/root/app.py")

if not streamlit_script_local_path.exists():
    raise RuntimeError(
        "app.py not found! Check your directory structure."
    )

streamlit_script_mount = modal.Mount.from_local_file(
    streamlit_script_local_path,
    streamlit_script_remote_path,
)

# Instantiate the Streamlit server
@app.function(
    allow_concurrent_inputs=100,
    mounts=[streamlit_script_mount],
)
@modal.web_server(8000)
def run():
    target = shlex.quote(str(streamlit_script_remote_path))
    cmd = f"streamlit run {target} --server.port 8000 --server.enableCORS=false --server.enableXsrfProtection=false"
    subprocess.Popen(cmd, shell=True)
