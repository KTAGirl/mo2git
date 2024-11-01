from mo2git.common import *

class ModList:
    def __init__(self,path):
        fname = path + 'modlist.txt'
        # print(fname)
        self.modlist = None
        with openModTxtFile(fname) as rfile:
            self.modlist = [line.rstrip() for line in rfile]
        self.modlist = list(filter(lambda s: s.endswith('_separator') or not s.startswith('-'),self.modlist))
        self.modlist.reverse() # 'natural' order
        # print(self.modlist)
        # dbgWait()

    def write(self,path):
        fname = path + 'modlist.txt'
        with openModTxtFileW(fname) as wfile:
            wfile.write("# This file was automatically modified by mo2git.\n")
            for line in reversed(self.modlist):
                wfile.write(line+'\n')
            
    def writeDisablingIf(self,path,f):
        fname = path + 'modlist.txt'
        with openModTxtFileW(fname) as wfile:
            wfile.write("# This file was automatically modified by mo2git.\n")
            for mod0 in reversed(self.modlist):
                if mod0[0]=='+':
                    mod = mod0[1:]
                    if f(mod):
                        wfile.write('-'+mod+'\n')
                    else:
                        wfile.write(mod0+'\n')
                else:
                    wfile.write(mod0+'\n')
    
    def allEnabled(self):
        for mod in self.modlist:
            if mod[0]=='+':
                yield mod[1:]
            
    def isSeparator(modname):
        if modname.endswith('_separator'):
            return modname[:len(modname)-len('_separator')]
        return None
        