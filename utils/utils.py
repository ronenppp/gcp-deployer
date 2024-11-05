import os
import random
import shutil
import string
import subprocess
import tempfile

from consts import DEPLOY_DEFAULT_LIBRARIES, DEV_FOLDER_NAME, REPO_FOLDER_NAME, COPY_BLACKLIST_FILES


def get_project_number(project_id: str) -> str:
    from google.cloud import resourcemanager_v3
    client = resourcemanager_v3.ProjectsClient()
    project_name = f"projects/{project_id}"
    project = client.get_project(name=project_name)
    return project.name.split("/")[1]  # Extract the project number


def prepare_deployment_folder(function_name: str) -> str:
    """Package all required code to one location"""
    source_folder_name = get_local_repo_path() + function_name
    target_folder_name = get_local_tmp_path() + os.sep + ''.join(['deploy_', generate_random_string(4), '_',
                                                                  function_name])
    copy_folder(source_folder_name, target_folder_name)

    for default_library in DEPLOY_DEFAULT_LIBRARIES:
        copy_folder(get_local_repo_path() + default_library, target_folder_name + os.sep + default_library + os.sep)

    return target_folder_name


def get_local_repo_path() -> str:
    """Return the local path to the development repo e.g. C:\\Users\\John\\PycharmProjects\\gcp-deployer\\ """
    return os.path.expanduser('~' + os.sep + DEV_FOLDER_NAME + os.sep + REPO_FOLDER_NAME + os.sep)


def generate_random_string(n: int) -> str:
    """Generate a random string by required length (n)"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def get_local_tmp_path() -> str:
    """Return the temp directory path for the current user"""
    root = os.path.dirname(os.path.abspath(__file__))
    tmp_path = tempfile.gettempdir()
    return os.path.join(root, tmp_path)


def copy_folder(source_folder: str, destination_folder: str) -> None:
    """Copy a folder in a recursive manner"""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    print(f'About to copy files from {source_folder} to {destination_folder}..')
    for root, dirs, files in os.walk(source_folder):
        # Create corresponding sub-folders in the destination folder
        relative_path = os.path.relpath(root, source_folder)
        destination_path = os.path.join(destination_folder, relative_path)
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        # Copy files to the destination folder
        for file in files:
            if file not in COPY_BLACKLIST_FILES:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_path, file)
                shutil.copy2(source_file, destination_file)


def run_tests(root_test_folder: str) -> bool:
    """Run all tests in the root test folder"""
    print(f'about to run unit tests on {root_test_folder}..')
    result = subprocess.run(['pytest', '-v', root_test_folder], capture_output=True, text=True)

    if result.returncode == 0:
        print(result.stdout)
        return True
    print(result.stderr)
    return False
