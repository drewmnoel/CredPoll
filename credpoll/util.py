import os


def get_cred_files(logs_dir: str) -> list:
    # Get files that contain hashes
    cred_files = []
    for file_name in os.listdir(logs_dir):
        # Exclude files ending in .log
        if file_name.split(".")[-1] != "log":
            cred_files.append(f"{logs_dir}/{file_name}")
    return cred_files


def get_hashes(cred_files: list) -> list:
    hashes = []
    for cred_file in cred_files:
        with open(cred_file, "r") as file:
            hashes += [line.strip() for line in file.readlines()]
    return hashes
