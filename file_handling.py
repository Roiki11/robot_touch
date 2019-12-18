class file:
    def loadFile(self):
            fname = qt.QFileDialog.getOpenFileName(self, 'Open file', '/Desktop')
            if fname:
                open_file = fname
                f = open(fname[0], 'r')
                for line in f:
                    self.programView.addItem(line)



    def saveFile(self):
        global open_file

        if open_file:
            file = open(open_file[0], 'w')
            items=[]
            for index in range(self.programView.count()):
                items.append(self.programView.item(index))

            for item in items:
                file.write(item.text())
            file.close()
        else:
            fname = qt.QFileDialog.getSaveFileName(self, 'Save File as', '/Desktop', '*.txt')
                if fname:
                    file = open(fname[0],'w')
                    items=[]
                    for index in range(self.programView.count()):
                        items.append(self.programView.item(index))

                    for item in items:
                        file.write(item.text())
                    file.close()

    def newFile(self):
        global open_file

        fname = qt.QFileDialog.getSaveFileName(self, 'Save File as', '/Desktop', '*.txt')
        if fname:
            file = open(fname[0],'w')
            text = '## Program Start##'
            file.write(text)
            open_file = fname
            self.programView.addItem(text)