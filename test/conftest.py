import pytest
import subprocess
import os

PROJECT_NAME = "ci-test-project-do-not-delete"
TEST_PROJECT_DIR = "test/data"

TEST_PROJECT_DIR_FULL_PATH = os.path.join(TEST_PROJECT_DIR, PROJECT_NAME)

@pytest.fixture(scope="session")
def divio_project():
    if not os.path.exists(TEST_PROJECT_DIR_FULL_PATH):
        subprocess.run(["divio", "project", "setup", PROJECT_NAME], cwd=TEST_PROJECT_DIR, check=True)
    return TEST_PROJECT_DIR_FULL_PATH
