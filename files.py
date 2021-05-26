import os


class Files:

    # Write data in json file
    def write_file(self, data):
        with open("data.json", "a+", encoding="utf-8") as f:
            f.write(f'{data},')

    # Delete json file when its create before to run the project
    def delete_json(self):
        if os.path.exists("data.json"):
            return os.remove("data.json")

    # Method to create json file that start with "[" for it take format of json
    def create_json_file(self):
        with open("data.json", "a+", encoding="utf-8") as f:
            f.write("[\n")
            f.close()

    # Open data.json and read, then validate if found
    def close_json_file(self):
        # If not exist file, show error and pass to next line, when read data.json file and then write in new file
        # called new_data.json
        try:
            os.remove("new_data.json")
        except FileNotFoundError as fn:
            print(fn)

        with open("data.json", "r+", encoding="utf-8") as input:
            with open("new_data.json", "a+", encoding="utf-8") as f:
                for line in input:
                    if line != "},":
                        f.write(line)
                f.write("}]")

    def student_exists(self, name):
        count = 0
        with open("data.json", "r+", encoding="utf-8") as f:
            for line in f:
                if name in line:
                    count += 1
            if count == 0:
                return True
            else:
                return False