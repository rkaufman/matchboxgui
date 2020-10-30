from flask import current_app as app

class MxserverPathConverter(object):

    def __init__(self, mxserver_mount_path):
        self.mxserver_mount_path = mxserver_mount_path
        self.saved_remote_path_prefix = None # This is set by convert_to_local_path()
        self.delimiter = None

    """
    Convert the path provided by MXSERVER in REST API request to a path that is mounted on MatchBox.
    NOTE: This must be called before convert_to_remote_image_path().
    """
    def convert_to_local_image_path(self, filename):
        # Delimiter is the last part of the path

        try:
            self.delimiter = self.mxserver_mount_path.rsplit('/', 1)[1]
            print("1111", self.delimiter)
            app.logger.info("MxserverPathConverter - self.delimiter: " + self.delimiter)
            input_file_slash = filename.replace('\\', '/')
            print("2222", input_file_slash)
            app.logger.info("MxserverPathConverter - input_file_slash: " + input_file_slash)
            saved_remote_path_prefix, path_suffix = input_file_slash.split(self.delimiter)
            print("3333", saved_remote_path_prefix)
            app.logger.info("MxserverPathConverter - saved_remote_path_prefix: " + saved_remote_path_prefix)
            saved_remote_path_prefix = saved_remote_path_prefix + self.delimiter
            print("4444", saved_remote_path_prefix)
            app.logger.info("MxserverPathConverter - saved_remote_path_prefix: " + saved_remote_path_prefix)

        except Exception as e:
            app.logger.error("Error convert_to_local_image_path: " + str(e))
            return "Error converting path"

        # We'll need this to reverse the operation, so save it
        self.saved_remote_path_prefix = saved_remote_path_prefix

        filename = self.mxserver_mount_path + path_suffix
        return filename

    """
    Convert the local path to MXSERVER path for sending path info back to MXSERVER.
    NOTE: convert_to_remote_image_path() must be called first.
    """
    def convert_to_remote_image_path(self, input_file):
        if self.saved_remote_path_prefix is None:
            print("saved_remote_path_prefix needs to be set. This method can only be run after convert_to_local_path()")
        if self.delimiter is None:
            print("delimiter needs to be set. This method can only be run after convert_to_local_path()")

        try:
            remote_path_prefix = self.saved_remote_path_prefix
            app.logger.info("convert_to_remote_image_path - self.saved_remote_path_prefix: " + self.saved_remote_path_prefix)
            path_suffix = input_file.split(self.delimiter)[1]
            app.logger.info("convert_to_remote_image_path - path_suffix: " + path_suffix)
            original_remote_file = remote_path_prefix + path_suffix
            app.logger.info("convert_to_remote_image_path - original_remote_file: " + original_remote_file)
            original_remote_file = original_remote_file.replace('/', '\\')
            app.logger.info("convert_to_remote_image_path - original_remote_file: " + original_remote_file)

        except Exception as e:
            app.logger.error("Error convert_to_remote_image_path: " + str(e))
            return "Error converting path"

        return original_remote_file

    """
    Convert the DIR path provided by MXSERVER in REST API request to a path that is mounted on MatchBox.
    NOTE: This must be called before convert_to_remote_image_path().
    """
    def convert_to_local_dir_path(self, output_directory):
        # Convert from Windows format
        output_directory_clean = output_directory.replace('\\', '/')
        # Get just the unique part of the dir path (after the delimiter)
        unique_directory_for_image = output_directory_clean.split(self.delimiter)[1]
        output_save_directory = self.mxserver_mount_path + unique_directory_for_image

        return output_save_directory
