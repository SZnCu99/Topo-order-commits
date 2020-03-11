
import os,sys,zlib


class Globals:
    def __init__(self):
        self.nodes = {}
        self.roots = {}
        self.sortedlist = []
        self.headdict = {}

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()


def isgit():
    path = '.'    
    while True:
        dir_list = next(os.walk(path))[1]
        for dirs in dir_list:
            if dirs == ".git":
                path = os.path.abspath(path)
                value = path+'/'+dirs
                return value
        if path != '/':
            path = os.path.abspath(os.path.join(path, os.pardir))      
        else:
            break
    return ""

def findparent(path,name):
    objpath = path + '/objects/'+ name[0:2] + '/' + name[2:]
    compressed = open(objpath,'rb').read()
    contents = zlib.decompress(compressed)
    ostr = str(contents, 'utf-8')
    parents = ""
    plist = []
    for s in ostr.split("\n"):
        if "parent" in s:
            parents = s;
            plist += parents.split()[1:]
    plist.sort()
    return plist


def addnode(path,stack,mglobal):
    visited = set()
    while(stack):
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        vnode = mglobal.nodes.get(v)
        if not vnode:
            vnode = CommitNode(commit_hash=v)
        plist = findparent(path,v)
        if plist:
            for p in plist:
                stack.append(p)
                vnode.parents.add(p)
                pnode = mglobal.nodes.get(p)
                if not pnode:
                    pnode = CommitNode(commit_hash=p)
                pnode.children.add(v)
                mglobal.nodes[p] = pnode
        mglobal.nodes[v] = vnode
    return

def buildgraph(path,mglobal):
    hpath = path + '/refs/heads'
    headlist = []
    for f in os.listdir(hpath):
        d = hpath+'/'+f
        head = open(d,'r').read()
        head = head.rstrip()
        headlist.append(head)
        mglobal.headdict[f] = head
    headlist.sort()   
    addnode(path,headlist,mglobal)

def toposort(stack,mglobal):
    visited = set()
    while(stack):
        toadd = True
        v = stack[-1]
        if v in mglobal.sortedlist:
            p = stack.pop()
            continue
        if v not in visited:
            visited.add(v)
        children = v.children
        if not children:
            mglobal.sortedlist.append(v)
            stack.pop()
            continue
        else:
            children = sorted(list(children))
            for c in children:
                cnode = mglobal.nodes[c]
                if cnode not in visited:
                    stack.append(cnode)
                    toadd = False
            if toadd:
                mglobal.sortedlist.append(v)
                stack.pop()

    return


def findtag(h,mglobal):
    tlist = ""
    for tag,head in mglobal.headdict.items():
        if head == h:
            tlist = tlist + tag + " "
    return tlist     


def printlist(mglobal):
    length = len(mglobal.sortedlist)
    seg = False

    for i in range (0,length):
        attach = ""
        node = mglobal.sortedlist[i]
        if seg is True:
            seg = False
            cstring = "="
            for c in node.children:
                cstring = cstring + c + " "
            if cstring:
                print (cstring)
        toprint = node.commit_hash
        if i != length - 1:
            nextnode = mglobal.sortedlist[i+1]
            if nextnode.commit_hash not in node.parents:
                seg = True
                attach = "\n"
                count = 0
                for p in node.parents:
                    if count != 0:
                        attach = attach + " " + p 
                    else:
                        attach = attach + p
                        count = 1
                attach = attach + "=\n"
#                print (toprint+attach)
            
            attach = " " + findtag(node.commit_hash,mglobal) + attach
        print (toprint + attach)
             



def topo_order_commits():
    mglobal = Globals()
    gitpath = isgit()
    if gitpath != "":
        buildgraph(gitpath,mglobal)

        for n in mglobal.nodes.values():
            if not n.parents:
                mglobal.roots[n.commit_hash] = n
     
        rootlist = list(mglobal.roots.values())

        toposort(rootlist,mglobal)
        printlist(mglobal)
    else:
        sys.stderr.write("Not inside a Git repository\n")
        exit(1)

if __name__ == '__main__':
    topo_order_commits()

