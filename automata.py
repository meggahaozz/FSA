# -*- coding: UTF-8 -*-
'''
    version: 0.8.0
    -creating FSA from input
    -determining FSA
    -minimizing FSA
    -drawing FSA
    -creating FSA from grammar [test mode]
    -save/load FSA in .fa format
    -test sequences feature
    -epsilon loops
    ### add tutorial

    ---------------------------------------
    Developed by Zorin Roman Anatolevich, Dubna University
'''
from Tkinter import *
from tkFont import Font
import ttk
import tkMessageBox
import tkFileDialog
import pydot_ng
import datetime
import time
from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *
from PIL import Image
import collections
import unicodedata
import mycnfbuilder as mcb
from string import letters
import copy

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.automaton = NFA()
        self.parent.title("Finite-State Automaton Handler v0.8.0")
        # initialize GUI
        self.menuBar = Menu(self.parent, background="#76d275", foreground='#97b498',
                            activebackground='#43a047', activeforeground='#97b498')
        self.parent.config(menu=self.menuBar)
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.load_file)
        self.fileMenu.add_command(label="Save", command=self.save_file)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.parent.quit)
        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="How to", command=self.howTo)
        self.helpMenu.add_command(label="About", command=self.about)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

        myFont = Font(family="Times New Roman", size=12, weight='bold')

        # type entry
        self.tpl = Label(self.parent, text="Type", font=myFont)
        self.tpe = Entry(self.parent, bd=5, width=40, bg="#c8e6c9", state=NORMAL, font=myFont)
        self.tpl.grid(row=0, column=0)
        self.tpe.grid(row=0, column=1)
        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=1, columnspan=5, sticky="ew")

        # states entry
        self.l1 = Label(self.parent, text="States", font=myFont)
        self.e1 = Entry(self.parent, bd=5, width=40, bg="#c8e6c9", state=NORMAL, font=myFont)
        self.l1.grid(row=2, column=0)
        self.e1.grid(row=2, column=1)
        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=3, columnspan=5, sticky="ew")
        # alphabet entry
        self.l2 = Label(self.parent, text="Alphabet", font=myFont)
        self.e2 = Entry(self.parent, bd=5, width=40, bg="#c8e6c9", state=NORMAL, font=myFont)
        self.l2.grid(row=4, column=0)
        self.e2.grid(row=4, column=1)
        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=5, columnspan=5, sticky="ew")
        # start entry
        self.l3 = Label(self.parent, text="Start", font=myFont)
        self.e3 = Entry(self.parent, bd=5, width=40, bg="#c8e6c9", state=NORMAL, font=myFont)
        self.l3.grid(row=6, column=0)
        self.e3.grid(row=6, column=1)
        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=7, columnspan=5, sticky="ew")
        # final entry
        self.l4 = Label(self.parent, text="Final", font=myFont)
        self.e4 = Entry(self.parent, bd=5, width=40, bg="#c8e6c9", state=NORMAL, font=myFont)
        self.l4.grid(row=8, column=0)
        self.e4.grid(row=8, column=1)
        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=9, columnspan=5, sticky="ew")
        # transition entry with add button
        self.l5 = Label(self.parent, text="Transitions", font=myFont)
        self.e5 = Text(self.parent, bd=5, width=30, height=10, bg="#c8e6c9", state=NORMAL, font=myFont)
        self.l5.grid(row=10, column=0)
        self.e5.grid(row=10, column=1)
        # self.e5.bind_class("Entry", "<Button-3><ButtonRelease-3>", self.show_menu)
        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=11, columnspan=5, sticky="ew")

        self.b1 = Button(self.parent, text="Create FSA", bd=5, bg="#76d275", font=myFont, command=self.getFSAFromInput)
        self.b1.grid(row=12, column=0)
        self.b7 = Button(self.parent, text="Create FSA from CFG", bd=5, bg="#76d275", font=myFont, command=self.CFGToFSA)
        self.b7.grid(row=12, column=1)
        self.b3 = Button(self.parent, text="Clear", bd=5, bg="#76d275", font=myFont, command=self.clearAll)
        self.b3.grid(row=12, column=2)

        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=13, columnspan=5, sticky="ew")
        # test word entry with button
        self.e6 = Entry(self.parent, bd=5, width=40, bg="#c8e6c9", state=NORMAL, font=myFont)
        self.e6.grid(row=14, column=0)
        self.b2 = Button(self.parent, text="Test word", bd=5, bg="#76d275", font=myFont, command=self.applyWordToFSA)
        self.b2.grid(row=14, column=1)
        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=15, columnspan=5, sticky="ew")

        # display img button
        self.b4 = Button(self.parent, text="Draw FSA", bd=5, bg="#76d275", font=myFont, command=self.displayImg)
        self.b4.grid(row=16, column=1)

        # minimize button
        self.b5 = Button(self.parent, text="Minimize FSA", bd=5, bg="#76d275", font=myFont, command=self.minimizeDFA)
        self.b5.grid(row=16, column=0)

        # determine button
        self.b6 = Button(self.parent, text="Determine", bd=5, bg="#76d275", font=myFont, command=self.determine)
        self.b6.grid(row=16, column=2)

        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=17, columnspan=5, sticky="ew")
        self.b7 = Button(self.parent, text="Add epsilon loops", bd=5, bg="#76d275", font=myFont, command=self.addEps)
        self.b7.grid(row=18, column=0)
        self.b8 = Button(self.parent, text="Eliminate epsilon loops", bd=5, bg="#76d275", font=myFont, command=self.elimEps)
        self.b8.grid(row=18, column=1)

        ttk.Separator(self.parent, orient=HORIZONTAL).grid(row=19, columnspan=5, sticky="ew")
        self.b9 = Button(self.parent, text="DFA from regex", bd=5, bg="#76d275", font=myFont, command=self.fromRe)
        self.b9.grid(row=20, column=0)

        print "gui initialized"


    # method that converts dfa to graph
    def dfsmToGraph(self, dfa):
        graph = pydot_ng.Dot(graph_type = 'digraph', orientation='landscape')

        states = list(dfa.States) # set of states, converting to list
        sigma = dfa.Sigma # set of symbols
        init = dfa.Initial # set of inits
        fin = dfa.Final # set of indexes of final states
        delta = dfa.delta # dict {0 : {'1' : 0, ...}, ...}

        graph.add_node(pydot_ng.Node('start', shape='point'))

        for k in states:
            if states.index(k) in fin:
                graph.add_node(pydot_ng.Node(states.index(k), shape="doublecircle"))
            else:
                graph.add_node(pydot_ng.Node(states.index(k), shape="circle"))

        if isinstance(init, collections.Iterable):
            for i in init:
                graph.add_edge(pydot_ng.Edge('start', i))
        else:
            graph.add_edge(pydot_ng.Edge('start', init))

        for key in delta:
            for k in delta[key]:
                # key is first state
                # k is symbol
                # delta[key][k] is a set of next states
                q = key
                a = k
                qs = delta[key][k]
                if isinstance(qs, collections.Iterable):
                    for qss in qs:
                        graph.add_edge(pydot_ng.Edge(q,qss,label=a))
                else:
                    graph.add_edge(pydot_ng.Edge(q,qs,label=a))

        return graph

    # method that tests word on dfa
    def applyWordToFSA(self):
        word = str(self.e6.get())
        for c in word:
            if c not in self.automaton.Sigma:
                tkMessageBox.showinfo("info", "Your word contains a wrong character!")
                return
        if self.automaton.evalWordP(word):
            tkMessageBox.showinfo("info", "Word %s is accepted" % str(word))
        else:
            tkMessageBox.showinfo("info", "Word %s is not accepted" % str(word))

    # method that converts user input to dfa
    def getFSAFromInput(self):
        self.automaton = NFA()
        states = list(str(self.e1.get()).split(' '))
        sigma = set(str(self.e2.get()).split(' '))
        tinit = set(str(self.e3.get()).split(' '))
        init = set(states.index(x) for x in tinit)
        tfin = set(str(self.e4.get()).split(' '))
        fin = set(states.index(x) for x in tfin)
        for s in states:
            self.automaton.addState(s)
        for s in sigma:
            self.automaton.addSigma(s)
        for i in init:
            self.automaton.addInitial(i)
        for f in fin:
            self.automaton.addFinal(f)
        text = str(self.e5.get('1.0', END)).splitlines()
        for line in text:
            ls = line.split(' ')
            if len(ls) != 3:
                tkMessageBox.showinfo("info", "Wrong input!")
                self.clearAll()
                return
            a = states.index(ls[0]) # index of fist state
            b = str(ls[1]) # symbol
            c = states.index(ls[2]) # index of second state
            if b =='eps':
                self.automaton.addTransition(a, Epsilon, c)
            else:
                self.automaton.addTransition(a, b, c)
        print "created"

    # method that loads dfa from file
    def load_file(self):
        ftypes = [('finite-state automata files', '*.fa'), ('All files', '*')]
        fil = tkFileDialog.askopenfilename(filetypes=ftypes)
        if fil:
            try:
                self.automaton = readFromFile(fil)[0]
                self.update()
                print "loaded"
            except Exception as ex:
                #tkMessageBox.showinfo("Open Source File", "Failed to read file\n'%s'" % f)
                tkMessageBox.showinfo("Open Source File", "exception %s" % ex)

    # method that saves dfa to file
    def save_file(self):
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension='.fa')
        if f is None:
            return
        s = fa.saveToString(self.automaton, sep='\n')
        f.write(s)
        f.close()
        print "saved"

    # method that displays graph
    def displayImg(self):
        graph = self.dfsmToGraph(self.automaton)
        hash = "FSA" + datetime.datetime.now().strftime("%I%M%d%m%Y") + ".png"
        graph.write_png(hash)
        image = Image.open(hash)
        image.show()
        print "displayed"

    def minimizeDFA(self):
        self.automaton = self.automaton.minimal()
        if 'dead' in self.automaton.States:
            self.automaton.deleteState(self.automaton.States.index('dead'))
        self.update()
        tkMessageBox.showinfo("info", "Your FSA is now minimal!")
        print "minimized"

    # context-free grammar to FSA
    def CFGToFSA(self):
        ruleStrings = str(unicodedata.normalize("NFKD", self.e5.get('1.0', END)).replace(u"\u03b5", "e").encode('ascii','ignore')).splitlines()
        rules = list() # list of tuples
        terminals = set() # lower; Sigma
        nonterminals = set() # upper; States
        for line in ruleStrings:
            r, l = [x.strip() for x in line.split("->")]
            prods = [p.strip() for p in l.split("|")]
            t = (r, prods)
            rules.append(t)
            nonterminals.add(r)
            for c in l:
                if c.isupper():
                    nonterminals.add(c)
                elif c != '|' and c != ' ' and c != 'e':
                    terminals.add(c)
        start = rules[0][0]
        newRules = {}
        voc = []
        let = list(letters[26:]) + list(letters[:25])
        let.remove('e')

        for r in rules:
            for prod in r[1]:
                fr = str(r[0])
                to = str(prod)
                # Remove given letters from "letters pool"
                for l in fr:
                    if l!='e' and l not in voc: voc.append(l)
                    if l in let: let.remove(l)
                for l in to:
                    if l!='e' and l not in voc: voc.append(l)
                    if l in let: let.remove(l)
                # Insert rule to dictionary
                newRules.setdefault(fr, []).append(to)
        newRules, let, voc = mcb.large(newRules, let, voc)
        newRules, voc = mcb.empty(newRules, voc)
        newRules, D = mcb.short(newRules, voc)
        newRules = mcb.final_rules(newRules, D, str(start))
        rules = list()
        for key in newRules:
            values = newRules[key]
            r = key
            prods = [x for x in values if 'e' not in x]
            t = (r, prods)
            rules.append(t)
        #print rules

        regular = True
        leftRG = False
        rightRG = False
        for leftSide, rightSide in rules:
            for nonterminal in nonterminals:
                if not(leftRG or rightRG):
                    if len(rightSide) > 1:
                        if (nonterminal in rightSide[0]):
                            leftRG = True
                        elif (nonterminal in rightSide[-1]):
                            rightRG = True
                        else:
                            regular = regular and not (nonterminal in rightSide)
                if rightRG:
                    regular = regular and not (nonterminal in rightSide[:-1])
                if leftRG:
                    regular = regular and not (nonterminal in rightSide[1:])

        # check for right sided or left sided
        if not rightRG and not leftRG:
            tkMessageBox.showinfo("info", "Cannot convert this grammar to automata!")
            return


        self.automaton = NFA()
        for s in nonterminals:
            self.automaton.addState(s)
        for s in terminals:
            self.automaton.addSigma(s)
        tinit = set()
        tinit.add(self.automaton.States.index(start))
        self.automaton.Initial = tinit
        for left, right in rules:
            for r in right:
                q = left
                a = [x for x in terminals if x in r]
                qs = [x for x in nonterminals if x in r]
                # wrong but who cares?
                if not qs:
                    if "Z" not in self.automaton.States:
                        self.automaton.addState("Z")
                        self.automaton.addFinal(self.automaton.States.index("Z"))
                    self.automaton.addTransition(self.automaton.States.index(q), a[0], self.automaton.States.index("Z"))
                else:
                    self.automaton.addTransition(self.automaton.States.index(q), a[0], self.automaton.States.index(qs[0])) # leeeeeeel
        # fix this
        self.update()
        print "converted"

    def update(self):
        self.clearAll()
        self.tpe.insert(0, str(type(self.automaton)).split('.')[2][:-2])
        self.e1.insert(0, " ".join(str(e) for e in self.automaton.States))
        self.e2.insert(0, " ".join(str(e) for e in self.automaton.Sigma))
        if isinstance(self.automaton.Initial, collections.Iterable):
            self.e3.insert(0, " ".join(str(self.automaton.States[e]) for e in self.automaton.Initial))
        else:
            self.e3.insert(0, str(self.automaton.States[self.automaton.Initial]))
        self.e4.insert(0, " ".join(str(self.automaton.States[e]) for e in self.automaton.Final))
        text = ""
        for key in self.automaton.delta:
            for k in self.automaton.delta[key]:
                # key is first state
                # k is symbol
                # delta[key][k] is a set of next states
                q = key
                a = k
                qs = self.automaton.delta[key][k]
                if isinstance(qs, collections.Iterable):
                    for qss in qs:
                        text += str(self.automaton.States[q]) + " " + a + " " + str(self.automaton.States[qss]) + '\n'
                else:
                    text += str(self.automaton.States[q]) + " " + a + " " + str(self.automaton.States[qs]) + '\n'
        self.e5.insert('1.0', text)
        print "updated"
        print str(type(self.automaton)).split('.')[2][:-2]

    # clears all entries
    def clearAll(self):
        self.tpe.delete(0, END)
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete('1.0', END)
        self.e6.delete(0, END)
        print "cleared"

    def determine(self):
        self.automaton = self.automaton.toDFA()
        self.update()
        print "determined"

    def howTo(self):
        # TODO add tutorial here
        tkMessageBox.showinfo("info", "Coming soon...")

    def about(self):
        tkMessageBox.showinfo("info", "Developed by Zorin R.A. 2017")

    def addEps(self):
        if isinstance(self.automaton, NFA):
            self.automaton.addEpsilonLoops()
        else:
            tkMessageBox.showinfo("info", "Can't add epsilon loops to DFA!")
        print "add eps"

    def elimEps(self):
        if isinstance(self.automaton, NFA):
            self.automaton.elimEpsilon()
        else:
            tkMessageBox.showinfo("info", "DFA doesn't have any epsylon loops!")
        print "elim eps"

    def fromRe(self):
        inp = str(self.e5.get('1.0', END))
        try:
            r = str2regexp(inp)
            self.automaton = r.toDFA()
            self.update()
            print "created from regex: " + str(r)
        except Exception as ex:
            tkMessageBox.showinfo("info", "Something wrong with your regex...")


    # TODO remove this shit when finish
    def donothing(self):
       filewin = Toplevel(self.parent)
       button = Button(filewin, text="Do nothing button")
       button.grid(row=0, column=0)


# main
root = Tk()
root.resizable(width=False, height=False)
app = MainApplication(root)
root.mainloop()
