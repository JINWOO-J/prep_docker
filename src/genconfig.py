#!/usr/bin/env python
import json
import sys,os,io,re
from itertools import chain
from collections import defaultdict

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

def merge_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def load_compose(filename="docker-compose.yml"):
    with open(path+"/"+filename, 'r') as stream:
        data_loaded = yaml.load(stream)
        dump(data_loaded)    
        return data_loaded

def write_compose(data, filename="docker-compose_tmp.yml"):
    with io.open(filename, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

def openJson(filename):
    if filename is None:
        filename = "FILENAME is NONE"
    try:
        json_data = open(filename).read()
    except:
        print("Error Openning json : " + filename)
        json_data = None
    try:
        result = json.loads(json_data)
    except:
        print("Error Decoding json : " + filename)
        result = {}
    return result


class dotdictify(dict):
    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError

    def __setitem__(self, key, value):
        doit = True
        if key[0] == '"' and key[-1] == '"':
            key = key.replace('"','')
            doit = True

        elif key[0] == "'" and key[-1] == "'":
            key = key.replace("'","")
            doit = True


        elif key is not None and '.' in key:
            myKey, restOfKey = key.split('.', 1)
            target = self.setdefault(myKey, dotdictify())
            if not isinstance(target, dotdictify):
                raise KeyError
            target[restOfKey] = value
            doit = False

        if doit:
            if isinstance(value, dict) and not isinstance(value, dotdictify):
                value = dotdictify(value)
            dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if key is None or '.' not in key:
            return dict.__getitem__(self, key)
        myKey, restOfKey = key.split('.', 1)
        target = dict.__getitem__(self, myKey)
        if not isinstance(target, dotdictify):
            raise KeyError
        return target[restOfKey]

    def __contains__(self, key):
        if key is None or '.' not in key:
            return dict.__contains__(self, key)
        myKey, restOfKey = key.split('.', 1)
        if not dict.__contains__(self, myKey):
            return False
        target = dict.__getitem__(self, myKey)
        if not isinstance(target, dotdictify):
            return False
        return restOfKey in target

    def setdefault(self, key, default):
        if key not in self:
            self[key] = default
        return self[key]

    def get(self, k, d=None):
        if dotdictify.__contains__(self, k):
            return dotdictify.__getitem__(self, k)
        return d

    __setattr__ = __setitem__
    __getattr__ = __getitem__


class bcolors:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    light_purple = '\033[94m'
    purple = '\033[95m'

    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'       

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'    
    
def CPrint(msg,color="green"):    
    print (getattr(bcolors, color) + '%s' %msg  + bcolors.ENDC)        

def writeEnv(filename, dict):    
    dump(dict)
    with open(filename, "w") as f:
        for i in dict.keys():            
            f.write(i + "=" +  str(dict[i]) + "\n")

def writeJson(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    if os.path.exists(filename):
        CPrint("[OK] Write json file -> %s, %s" %(filename, file_size(filename)))

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    def_spacing = '   '

    if type(obj) == dict:
        print ('%s{' % ( def_spacing + (nested_level) * spacing ))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print ( bcolors.OKGREEN + '%s%s:' % (def_spacing +(nested_level + 1) * spacing, k) + bcolors.ENDC, end="")                
                dump(v, nested_level + 1, output)                
            else:        
                print ( bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s' % v + bcolors.ENDC, file=output)
        print ('%s}' % ( def_spacing + nested_level * spacing), file=output)
    elif type(obj) == list:
        print  ('%s[' % (def_spacing+ (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print ( bcolors.WARNING + '%s%s' % ( def_spacing + (nested_level + 1) * spacing, v) + bcolors.ENDC, file=output)
        print ('%s]' % ( def_spacing + (nested_level) * spacing), file=output)
    else:
        print (bcolors.WARNING + '%s%s' %  ( def_spacing + nested_level * spacing, obj) + bcolors.ENDC)

def is_hex(s):
    try:
        int(s, 16)
    except:
        return False
    return True


def str2bool(v):
    if type(v) == bool:
        return v
    elif type(v) == str:
        return v.lower() in ("yes", "true", "t", "1", "True", "TRUE")
    else:
        return eval(f"{v}") in ("yes", "true", "t", "1", "True", "TRUE")


def main():
    user_defined_env = os.environ.get("USER_DEFINED_ENV")
    if user_defined_env:
        user_defined_env_list = user_defined_env.split("\n")
        envSettings = {}
        for i,env in enumerate(user_defined_env_list):
            if len(env) > 0:
                config_setting, config_group = env.split("|")

                config_group = str(config_group).strip()
                if config_setting is None:
                    print(f"config_setting is None => {config_setting}")
                if config_group is None:
                    print(f"config_file is None => {config_group}")

                vars_name, vars_value = str(config_setting).strip().split("=")
                vars_name = str(re.sub(r"^\.", "", vars_name)).strip()
                vars_value = str(vars_value).strip()
                value_type = "string"

                if vars_value in "\"":
                    value_type = "string"
                if vars_value.isdigit():
                    vars_value = int(vars_value)
                    value_type = "int"
                elif vars_value in ("True", "TRUE", "False", "FALSE"):
                    vars_value = str2bool(vars_name)
                    value_type = "boolean"

                if envSettings.get(config_group) is None:
                    envSettings[config_group] = []

                envSettings[config_group].append( {"name": vars_name, "value": vars_value, "value_type": value_type} )
        # dump(envSettings)
        for config_group, values in envSettings.items():
            for i, value in enumerate(values):
                vars_name = value.get("name")
                vars_value = value.get("value")
                value_type = value.get("value_type")
                config_file = os.environ.get(config_group)
                if config_file:
                    print(f"[{i}] [{config_file}] position={vars_name}, value={vars_value}, type={value_type}")
                    prev_json = openJson(config_file)
                    # prev_json = dotdictify(openJson(config_file))
                    next_json = dotdictify({})
                    next_json.__setitem__(vars_name, vars_value)
                    changed_json = dict(next_json)
                    merge_json = merge_dicts( prev_json, changed_json)
                else:
                    print(f"{config_group} file or environment not found")
            if config_file:
                writeJson(config_file, merge_json)

if __name__ == '__main__':    
    main()
