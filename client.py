from cli import window

w = window()
while True:
    w.updateAndDraw()
    w.getCmd()
    if not w.eval():
        break
print "TERMINATED"
