from utils import project_root
import os
import shutil

# Install dependencies (if needed)
os.chdir(os.path.join(project_dir, "build", "pyscript", "pyscript.core"))
os.system("npm install")

# Build the project
os.chdir(os.path.join(project_dir, "build", "pyscript"))
os.system("make build")

# Check if the 'pyscript' package exists
test_pyscript = os.path.exists(os.path.join(project_dir, "packages", "pyscript"))
if test_pyscript:
    shutil.rmtree(os.path.join(project_dir, "packages", "pyscript"))

# Copy the built files
shutil.copytree(
    os.path.join(project_dir, "build", "pyscript", "pyscript.core", "dist"),
    os.path.join(project_dir, "packages", "pyscript"),
)
