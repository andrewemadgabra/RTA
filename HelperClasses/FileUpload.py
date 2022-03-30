import random
import string
import os


class File(object):

    @classmethod
    def get_random_string(cls, length=10):
        letters = string.ascii_letters + string.digits
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    @classmethod
    def upload_file(cls, file_name, file, base_dir, extention):
        file_path = os.path.join(
            base_dir, file_name + File.get_random_string() + '.' + extention)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file_path
