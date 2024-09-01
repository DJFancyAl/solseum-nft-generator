import os

def rename_files(directory):
    """Renames all files in the specified directory.

    Args:
        directory (str): The path to the directory containing the files.
    """
    directory = os.path.abspath(directory)

    for filename in os.listdir(directory):
        # Get the current file path
        file_path = os.path.join(directory, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Get the file extension
            file_ext = os.path.splitext(filename)[1]

            # # Generate a new filename (e.g., adding a prefix or suffix)
            new_filename = filename.replace(" - ", "-")

            # # Create the new file path
            new_file_path = os.path.join(directory, new_filename)

            # # Rename the file
            os.rename(file_path, new_file_path)

            print(f"Renamed {filename} to {new_filename}")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    rename_files(directory)