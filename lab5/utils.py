import tarfile

def extract_tar_gz(file_path, extract_path='.'):
    """
    Extracts a tar.gz file to the specified directory.

    :param file_path: Path to the tar.gz file.
    :param extract_path: Directory where the contents will be extracted.
    """
    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(path=extract_path)

# Example usage
file_path = 'network_part_2/facebook.tar.gz'
extract_path = '.'
extract_tar_gz(file_path, extract_path)