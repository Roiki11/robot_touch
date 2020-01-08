open_program=[]
class fileHandling:
    
    def loadFile(self):
        global open_program
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/Desktop')
        if fname:
            open_file = fname
            f = open(fname[0], 'r')
            open_program =[]
            for line in f:
                self.programView.addItem(line)
                open_program.append(line)



    def saveFile(self):
        global open_file
        global open_program

        if open_file:
            file = open(open_file[0], 'w')
            for item in open_program:
                file.write(item.text())
            file.close()
        else:
                open_file = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File as', '/Desktop', '*.txt')
                if open_file:
                    file = open(open_file[0],'w')
                    for item in open_program:
                        file.write(item.text())
                    file.close()

    def newFile(self):
        global open_file

        open_file = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File as', '/Desktop', '*.txt')
        if open_file:
            file = open(open_file[0],'w')
            text = '## Program Start##'
            file.write(text)
            self.programView.addItem(text)