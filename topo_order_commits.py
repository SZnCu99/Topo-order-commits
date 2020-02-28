# Keep the function signature,
# but replace its body with your implementation
import os,sys,zlib

#def topo_order_commits():
#    raise NotImplementedError

#nodes = {}
#roots = {}
#sortedlist = []
#headdict = {}

#i = []

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
#    def __hash__(self):
#        return hash(self.commit_hash)
#
#    def __eq__(self,other):
#        return self.commit_hash == other.commit_hash

def isgit():
    path = '.'    
#    print (path)
    while True:
        dir_list = next(os.walk(path))[1]
        for dirs in dir_list:
#            for d in dirs:
#            print (dirs)
            if dirs == ".git":
                path = os.path.abspath(path)
                value = path+'/'+dirs
#                print(value)
                return value
        if path != '/':
            path = os.path.abspath(os.path.join(path, os.pardir))
#            print (path)        
        else:
            break
    return ""

def findparent(path,name):
    objpath = path + '/objects/'+ name[0:2] + '/' + name[2:]
#    print(objpath)
    compressed = open(objpath,'rb').read()
    contents = zlib.decompress(compressed)
    ostr = str(contents, 'utf-8')
#    print (name)
#    print (ostr)
    parents = ""
    plist = []
    for s in ostr.split("\n"):
        if "parent" in s:
            parents = s;
#    print (parents)
            plist += parents.split()[1:]
    plist.sort()
    return plist

#def findchild(path,name):
#    objpath = path + '/objects/'+ name[0:2] + '/' + name[2:]
##    print(objpath)
#    compressed = open(objpath,'rb').read()
#    contents = zlib.decompress(compressed)
#    ostr = str(contents, 'utf-8')
#    print (ostr)
#    children = ""
#    for s in ostr.split("\n"):
#        if "child" in s:
#            children = s;
##    print (parents)
#    clist = children.split()[1:]
#    return clist


def addnode(path,stack,mglobal):
#    node = CommitNode(commit_hash=name)
#    print ("my SHA1:")
#    print (node.commit_hash)
#    plist = findparent(path, name)
#    if plist:
#        for p in plist:
#            node.parents.add(p)
##            print ("my parents:")
##            print (node.parents)
#            pnode = mglobal.nodes.get(p)
#            if not pnode:
#                pnode = CommitNode(commit_hash=p)
#                pnode.children.add(name)        
#                addnode(path,p,pnode,mglobal)
#            else:
##                print("adding child to " + p)
#                pnode.children.add(name)
##                pnode.children.sort()
##                print(pnode.children)
#                mglobal.nodes[p] = pnode
##    clist = findchild(path, name)
##    for c in clist:
##        node.children.add(c)
#
#    mglobal.nodes[node.commit_hash] = node
##    print("\n")
#    return
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
#    nodes = []
    for f in os.listdir(hpath):
        d = hpath+'/'+f
        head = open(d,'r').read()
        head = head.rstrip()
#        print (head)
        headlist.append(head)
        mglobal.headdict[f] = head
#        print("")
    headlist.sort()

#        plist = findparent(path,h)
#        print (plist)
#        node = CommitNode(commit_hash=h)
#        for p in plist:
#            node.parents.add(p)
#        nodes.append(node)
#        print (node.commit_hash)
#        print (node.parents)
#        hnode = mglobal.nodes.get(h)
#        if not hnode:
#            hnode = CommitNode(commit_hash=h)
#            addnode(path, h, hnode,mglobal)    
    addnode(path,headlist,mglobal)

def toposort(stack,mglobal):
#    print (root.commit_hash)
#    count = 0
#    if root.children:
#        for c in sorted(list(root.children)):
#            cnode = mglobal.nodes[c]
#            if count != 0:
#                newlist = [root]
#                toposort(cnode,newlist,mglobal)
#            else:
#                slist.append(root)
#                toposort(cnode,slist,mglobal)    
#                count = 1
#    else:
#        slist.append(root)
#        mglobal.sortedlist.append(slist)
#        return
    visited = set()
#    for i in stack:
#        print (i)
    while(stack):
        toadd = True
        v = stack[-1]
#        print ("popping: ")
#        print (v)
        if v in mglobal.sortedlist:
            p = stack.pop()
#            print (p.commit_hash)
 #           print (stack)
            continue
        if v not in visited:
            visited.add(v)
#            print ("visited: ")
#            print (v.commit_hash)
#        stack.append(v)
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
#                    print("adding node:")
#                    print(cnode.commit_hash)
                    toadd = False
            if toadd:
                mglobal.sortedlist.append(v)
                stack.pop()
#                continue

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
#        print (gitpath)
        buildgraph(gitpath,mglobal)

        for n in mglobal.nodes.values():
#            print (n.commit_hash)
#            print ("parents: ")
#            print (n.parents)
#            print ("children: ")
#            print (n.children)
#            print ("\n")
            if not n.parents:
                mglobal.roots[n.commit_hash] = n

#        for r in mglobal.roots.values():
##            print (r.commit_hash)
#            mylist = []
#            toposort(r,mylist,mglobal)
#        print("```")        
        rootlist = list(mglobal.roots.values())
#        print (rootlist)
        toposort(rootlist,mglobal)
#        for n in mglobal.sortedlist:
#             print(n.commit_hash)
        printlist(mglobal)
#        count = 0
#        attach = ""
#        listsize = len(mglobal.sortedlist)
#        for l in mglobal.sortedlist:
#            l.reverse()
##            print (l)
#            if l != mglobal.sortedlist[0]:
#                print ("=")
#            length = len(l)
#            counter = 0
#            for node in l:
#                if counter != length - 1:
#                    attach = " " + findtag(node.commit_hash,mglobal)    
#                else:
#                    if count != listsize -1:
#                        attach = "="
#                print (node.commit_hash+attach)
#                counter = counter + 1
#            if count != listsize - 1:
#                print("")
#            count = count + 1
##        print("```")
    else:
        sys.stderr.write("Not inside a Git repository\n")
        exit(1)

if __name__ == '__main__':
    topo_order_commits()

