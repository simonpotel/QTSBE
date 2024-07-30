import os

def list_files_in_directory(directory, extension):
    """Get files of a directory and its subdirectories without their extension"""
    files = []
    for root, dirs, files_in_dir in os.walk(directory):
        for file_name in files_in_dir:
            if file_name.endswith(extension):  # Only consider files with the specified extension
                relative_path = os.path.relpath(os.path.join(root, file_name), directory)
                name_without_extension = os.path.splitext(relative_path)[0].replace(os.sep, '_')
                files.append(name_without_extension)
    return files or ['None']
