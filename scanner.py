import os
import logging

def scan(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        logging.error(f"Directory '{path}' not found or is not a directory.")
        return

    try:
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                os.system(f"clamscan {file_path}")
    except Exception as e:
        logging.error(f"Error executing 'clamscan' on '{file_path}': {str(e)}")

# Testing the function with a directory
if __name__ == "__main__":
    directory = "downloads.lnk"
    scan(directory)