import random, pickle
import sys, os, string, shutil
import re, pathlib

RES_DIR = os.path.join(os.path.dirname(sys.argv[0]),'png')

class SaveFiles():
    def __init__(self):
        pass

    def initialize(self,home_dir):
        self.make_tmpdir(home_dir)
        self.make_commandfile()

    def make_tmpdir(self,home_dir):
        self.dirname = os.path.join(home_dir,self.randomname(10))
        os.makedirs(self.dirname)
        if os.name == "nt": #windows convert \\ to /
            pldir = pathlib.Path(self.dirname)
            self.dirname = pldir.as_posix()

    def make_commandfile(self):
        self.logfilename = os.path.join(self.dirname,'command.py')
        with open(self.logfilename, 'w', encoding='utf-8') as f:
            pass
        
    def save_command(self,command,fileparse=False):
        exclude = ["edit()","initialize()", "update_command()","savefig"]
        for e in exclude:
            if e in command:
                return
        if fileparse:
            command = command.replace("'",'"')
            match = re.findall(r'"(.*?)"',command)
            print(match)
            for filename in match:
                if filename == '.':
                    continue
                if os.path.isfile(filename):
                    filename = os.path.abspath(filename)
                    savedname = os.path.join(self.dirname, self.splittedfile(filename))
                    os.makedirs(os.path.dirname(savedname),exist_ok=True)
                    shutil.copy(filename, savedname)
                    command = command.replace('"{}"'.format(filename,),"os.path.join(savedir,\"{}\")".format(self.splittedfile(filename),))
                if os.path.isdir(filename):
                    filename = os.path.abspath(filename)
                    savedname = os.path.join(self.dirname, self.splittedfile(filename))
                    os.makedirs(os.path.dirname(savedname),exist_ok=True)
                    shutil.copytree(filename, savedname)
                    command = command.replace('"{}"'.format(filename,),"os.path.join(savedir,\"{}\")".format(self.splittedfile(filename),))
        with open(self.logfilename,'a', encoding='utf-8') as f:
            print(command,file=f)
            print("update_alias()",file=f)

    def save_npdata(self,new_name,data):
        pickle.dump(data,open(os.path.join(self.dirname,new_name),'wb'))
        with open(self.logfilename,'a') as f:
            print("{} = pickle.load(open(os.path.join(savedir,\"{}\"),\"rb\"))".format(new_name,new_name),file=f)
            print("justnow = {}".format(new_name,),file=f)
            print("update_alias()",file=f)

    def save_plot(self, new_name, figaxid, data, label):
        pickle.dump(data,open(os.path.join(self.dirname,new_name),'wb'))
        with open(self.logfilename,'a') as f:
            print("_ = pickle.load(open(os.path.join(savedir,\"{}\"),\"rb\"))".format(new_name,),file=f)
            print("lines = []",file=f)            
            print("for i in range(1,len(_)):",file=f)
            print(f"    line, = figs[{figaxid['figs']}].axes[{figaxid['axes']}].plot(_[0],_[i],label=\"{label}\")",file=f)
            print("    lines.append(line)",file=f)
            print("{} = lines if len(lines) > 1 else lines[0]".format(new_name,),file=f)
            print("justnow = {}".format(new_name,),file=f)
            print("update_alias()",file=f)

    def save_customloader(self,lis):
        functionname = lis[0]
        filename = lis[1]
        newname = lis[3]
        figaxid = lis[4]
        filename = os.path.abspath(filename)
        savedname = os.path.join(self.dirname, self.splittedfile(filename))
        print(filename)
        os.makedirs(os.path.dirname(savedname),exist_ok=True)
        if os.path.isfile(filename):
            shutil.copy(filename,savedname)
        if os.path.isdir(filename):
            shutil.copytree(filename,savedname)
        with open(self.logfilename,'a', encoding='utf-8') as f:
            print(f"{newname} = {functionname}(os.path.join(savedir,\"{self.splittedfile(filename)}\"),figs[{figaxid['figs']}].axes[{figaxid['axes']}])",file=f)
            print("justnow = {}".format(newname,),file=f)
            print("update_alias()",file=f)

    def splittedfile(self, filename):
        fp = os.path.splitdrive(filename)[1]
        if os.name == "nt": #windows convert \\ to /s
            plfp = pathlib.Path(fp)
            fp = plfp.as_posix()
        return fp[1:]

    def randomname(self,n):
        randlst = [random.choice(string.ascii_lowercase) for i in range(n)]
        return 'jem_' + ''.join(randlst)

    def remove_tmpdir(self):
        shutil.rmtree(self.dirname)

    def save(self,filepath):
        shutil.make_archive(filepath, format='zip', root_dir=self.dirname)
        shutil.move(filepath + ".zip", filepath)

    def open(self,filepath):
        shutil.unpack_archive(filepath,format='zip',extract_dir=self.dirname)

    def load(self):
        with open(self.logfilename, 'r', encoding='utf-8') as f:
            command = f.read()
        return command

    def load_command_py(self):
        with open(self.logfilename,"r", encoding='utf-8') as f:
            command = f.read()
        return command

    def save_log(self,log):
        pickle.dump(log,open(os.path.join(self.dirname,"log"),'wb'))

    def load_log(self):
        with open(os.path.join(self.dirname,"log"),'rb') as f:
            log = pickle.load(f)
        return log

    def save_axesproperties(self, values):
        with open(self.logfilename,'a', encoding='utf-8') as f:
            print(f"set_axesproperties({values})",file=f)

    def save_lineproperties(self, line_id, properties):
        with open(self.logfilename,'a', encoding='utf-8') as f:
            print(f"set_lineproperties({line_id},{properties})",file=f)

    def save_linemove(self, old_id, new_id):
        with open(self.logfilename, "a", encoding='utf-8') as f:
            print(f"move_line({old_id},{new_id})",file=f)

    def save_subplotsparam(self, is_tight, fig_id, parameters):
        with open(self.logfilename, "a", encoding='utf-8') as f:
            print(f"figs[{fig_id}].set_tight_layout({is_tight})",file=f)
            if is_tight:
                print(f"figs[{fig_id}].tight_layout()",file=f)
            else:
                print(f"figs[{fig_id}].subplots_adjust({parameters})",file=f)

savefile = SaveFiles()