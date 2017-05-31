#! /usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
"""
implementation of AppShell GUI application framework.

"""
#

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import  Pmw
from    AppShell        import AppShell
from    tkMessageBox    import showinfo

class AppShellMore(AppShell):
    #
    def __init__(self, **kw):
        #
        AppShell.__init__( self, **kw )


    def createMenuBar(self):
        self.menuBar.addmenuitem('File', 'command', 'Quit this application',
                                label='Quit',
                                command=self.root.quit )
        #
        self.menuBar.addmenu('Edit', 'Editing commands')
        #
        self.menuBar.addmenuitem(
            'Edit', 'command', 'cut text',   label = 'Cut',   command = self.NotImplemented )
        self.menuBar.addmenuitem(
            'Edit', 'command', 'copy text',  label = 'Copy',  command = self.NotImplemented )
        self.menuBar.addmenuitem(
            'Edit', 'command', 'paste text', label = 'Paste', command = self.NotImplemented )
        #
        # self.menuBar.addmenu('Help', 'About %s' % self.appname ) # , side='right'
        # self.menuBar.addmenuitem('Help', 'command',
        #                             'Get information on application', 
        #                             label='About...', command=self.showAbout)
        # self.toggleBalloonVar = IntVar()
        # self.toggleBalloonVar.set(1)
        # self.menuBar.addmenuitem('Help', 'checkbutton',
        #                             'Toggle balloon help',
        #                             label='Balloon help',
        #                             variable = self.toggleBalloonVar,
        #                             command=self.toggleBalloon)


    def NotImplemented(self):
        #
        showinfo( 'Not Implemented', 'The feature you selected is not implemented yet!' )



def doNothing():
    pass



class TestAppShell(AppShellMore):
        usecommandarea=1

        def createButtons(self):
                self.buttonAdd('Ok',
                        helpMessage='Exit',
                        statusMessage='Exit',
                        command=self.root.quit )

        def createMain(self):
                self.label = self.createcomponent('label', (), None,
                                        Label,
                                        (self.interior(),),
                                        text='Data Area')
                self.label.pack()
                self.bind(self.label, 'Space taker')

        def createInterface(self):
                AppShell.createInterface(self)
                # self.createButtons()
                self.createMain()

if __name__ == '__main__':
        test = TestAppShell(balloon_state='both')
        test.run()
