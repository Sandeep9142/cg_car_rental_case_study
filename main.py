import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.pipeline.pipeline_runner import run_pipeline


def main():
    dirs = [
        os.path.join(PROJECT_ROOT, "data", "raw"),
        os.path.join(PROJECT_ROOT, "data", "output"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    result = run_pipeline(project_root=PROJECT_ROOT)
    return result


if __name__ == "__main__":
    main()
