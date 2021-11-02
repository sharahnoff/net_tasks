import time


class Cache:
    def __init__(self, cache_file_name):
        self.cache_file_name = cache_file_name
        self.data = dict()

    def init(self):
        with open(self.cache_file_name) as f:
            for line in f.readlines():
                line = line.rstrip("\n").split(" ")
                name = line[0]
                if name not in self.data:
                    self.data[name] = dict()
                self.data[name][int(line[1])] = line[2:]

    def flush(self): #проверка истекших записей и сохранение на диск
        new_data = dict()
        with open(self.cache_file_name, 'w') as f:
            for key, value in self.data.items():
                for kkey, vvalue in value.items():
                    if float(vvalue[2]) > time.time():
                        f.write(f'{key} {kkey} {" ".join(map(str, vvalue))}\n')
                        if key not in new_data.keys():
                            new_data[key] = dict()
                        new_data[key][int(kkey)] = vvalue
        self.data = new_data

    def add_or_update(self, name, rtype, data):
        if name not in self.data.keys():
            self.data[name] = dict()
        self.data[name][rtype] = data
        self.flush()