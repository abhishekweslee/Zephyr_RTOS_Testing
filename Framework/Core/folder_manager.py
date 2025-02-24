import os
import shutil
import stat


class FolderManager:
    def __init__(self, source_folder, destination_folder):
        """
        Initializes the FolderManager with source and destination paths.

        :param source_folder: The folder to be copied.
        :param destination_folder: The location where the folder should be copied.
        """
        self.source_folder = source_folder
        self.destination_folder = destination_folder

    def copy_folder(self):
        """
        Copies the source folder to the destination with error handling.
        """
        try:
            if not os.path.exists(self.source_folder):
                raise FileNotFoundError(f"Source folder '{self.source_folder}' does not exist.")

            if os.path.exists(self.destination_folder):
                print(f"Destination folder '{self.destination_folder}' already exists. Removing it first.")
                self.delete_folder()

            shutil.copytree(self.source_folder, self.destination_folder)
            print(f"Copied '{self.source_folder}' to '{self.destination_folder}'")

        except Exception as e:
            print(f"Error copying folder: {e}")

    def grant_permissions(self):
        """
        Grants full read, write, and execute permissions (777) to the destination folder recursively.
        """
        try:
            if not os.path.exists(self.destination_folder):
                raise FileNotFoundError(f"Destination folder '{self.destination_folder}' does not exist.")

            for root, dirs, files in os.walk(self.destination_folder):
                for directory in dirs:
                    dir_path = os.path.join(root, directory)
                    os.chmod(dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                for file in files:
                    file_path = os.path.join(root, file)
                    os.chmod(file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

            os.chmod(self.destination_folder, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            print(f"Granted 777 permissions to '{self.destination_folder}'")

        except Exception as e:
            print(f"Error setting permissions: {e}")

    def delete_folder(self):
        """
        Deletes the destination folder with error handling.
        """
        try:
            if os.path.exists(self.destination_folder):
                shutil.rmtree(self.destination_folder)
                print(f"Deleted folder '{self.destination_folder}'")
            else:
                print(f"Folder '{self.destination_folder}' does not exist. Nothing to delete.")
        except Exception as e:
            print(f"Error deleting folder: {e}")


# Example Usage
# if __name__ == "__main__":
#     source = "/path/to/source/folder"
#     destination = "/path/to/destination/folder"
#
#     manager = FolderManager(source, destination)
#     manager.copy_folder()
#     manager.grant_permissions()
#
#     # Perform your work here
#
#     manager.delete_folder()
