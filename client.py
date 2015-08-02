from cli import window

w = window()
while True:
    w.updateAndDraw()
    if not w.getChar():
        break
print "TERMINATED"
