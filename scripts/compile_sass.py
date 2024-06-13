from utils import project_root
import os


def compile_sass():
    os.system(f"sass {project_root}/sass/index.sass {project_root}/public/index.css")
