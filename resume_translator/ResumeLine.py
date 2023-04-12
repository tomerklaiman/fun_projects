class ResumeLine:


    def __init__(self):
        self.text = ""
        self.x0 = []
        self.x1 = []
        self.y0 = []
        self.y1 = []

    def getText(self):
        return self.text

    def isEmpty(self):
        return len(self.x0) == 0

    def addData(self,text,x0,x1,y0,y1):
        self.text+= " "+text
        self.x0.append(x0)
        self.x1.append(x1)
        self.y0.append(y0)
        self.y1.append(y1)

