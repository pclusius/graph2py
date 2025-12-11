import matplotlib.pyplot as plt
import numpy as np
import sys
import PIL
PIL.Image.MAX_IMAGE_PIXELS = 933120000

fig = plt.figure()
ax = fig.add_subplot(111)

plt.setp(ax.get_xticklabels(), visible=False)
plt.setp(ax.get_yticklabels(), visible=False)
c = 'r'
size = 10
# ax.set_xlim([0, 10])
# ax.set_ylim([0, 10])

if len(sys.argv)<=1:
    print("To use this script, give the path to the source plot as a command line option.")
    print("The path mmust point to a valid bitmap (png, jpg, gif).")
    print("NOTE:")
    print("Start Python with interactive mode: python3 -i %s"%sys.argv[0])
    quit()
else:
    path_to_im=sys.argv[1]

img = plt.imread(path_to_im)
w = img.shape[1]
h = img.shape[0]
ax.imshow(img, extent=[0, w, 0, h])
pix = False
oclick = True
xclick = True
yclick = True
datax = []
datay = []
pointsx = []
pointsy = []
dx = []
dy = []
lengths = []
colors = []
last = None
locked=False
caps_on=False
dx0 = None
dy0 = None

def save_data(file=path_to_im+'.txt'):
	M = np.zeros((len(datax),2 ))
	M[:,0] = datax
	M[:,1] = datay
	np.savetxt(file,M,fmt='%.8e', header='x            y')
	print('Saved datax and datay in file '+file)
	return M

def lock_on(event):
    global locked,dx,dy,dx0,dy0
    if event.key=='shift':
        locked=True
        dx0 = None
        dy0 = None
def lock_off(event):
    global locked,dx,dy,dx0,dy0,lengths,points
    if event.key=='shift':
        locked=False
        if dx0 != None and dy0 != None:
            dx.append(datax[-1]-dx0)
            dy.append(datay[-1]-dy0)
            lengths.append(np.sqrt(dx[-1]**2+dy[-1]**2))
            if pix: points.set_offsets(np.array([pointsx,pointsy]).T)


def onclick(event):
    global oclick, xclick, yclick, origopixels, xpix, ypix, datax,datay, pointsx,pointsy,last,locked,pix,dx,dy,dx0,dy0,change_size
    if event.inaxes != ax: return
    if pix and not locked:
        # print(event.ydata, event.xdata)
        colors.append( img[int(event.ydata), int(event.xdata),:])
        print('saving color (press shift to measure)')
        return
    if oclick:
        origopixels = event.xdata, event.ydata
        # print(origopixels)
        oclick = False
    elif xclick:
        xpix = event.xdata
        xclick = False
    elif yclick:
        ypix = event.ydata
        yclick = False
    else:
        curx = (event.xdata-origopixels[0])/(xpix-origopixels[0])*(xx-origo[0]) + origo[0]
        cury = (event.ydata-origopixels[1])/(ypix-origopixels[1])*(yy-origo[1]) + origo[1]
        datax.append(curx)
        datay.append(cury)
        pointsx.append(event.xdata)
        pointsy.append(event.ydata)
        print('Data point: x=%8.4f, y=%8.4f' %(curx, cury))
        if dx0 == None: dx0 = datax[-1]
        if dy0 == None: dy0 = datay[-1]
        if not pix: last = ax.plot(event.xdata,event.ydata, marker='+', markersize=size, c=c)
        # print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #       (event.bdatautton, event.xdata, event.ydata, event.xdatadata, event.ydatadata))

cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid2 = fig.canvas.mpl_connect('key_press_event', lock_on)
cid3 = fig.canvas.mpl_connect('key_release_event', lock_off)

plt.ion()
plt.tight_layout()
plt.show()

if len(sys.argv) == 3 and sys.argv[2] == '--pixels':
    print('--pixels is on, using left bottom as origo, and no scaling')
    pix = True
    xx = w
    yy = h
    xpix = w
    ypix = h
    oclick = False
    xclick = False
    yclick = False
    origo = (0,0)
    origopixels = (0,0)
else:
    origo = input("""
    First we must locate the origo in the plot.
    If the plot axises start from (0,0), click on the origo, switch to this screen and hit Enter.
    If the plot axises do not start from (0,0), click on the "smallest corner" and give the lower bounds here
    as a pair of numbers (tuple), e.g. 100,120:\n""")
    if origo == '':
        origo = (0,0)
    else: origo = tuple(float(i) for i in origo.split(','))
    xx = float(input('In the image, click somewhere close to horisontal axis where there is a number, and insert that number here as input:\n'))
    yy = float(input('Now same with vertical axis, and insert that number here as input:\n'))
print(origo, xx,yy)
print('Now you can start clicking at the data points in the figure.')
print("   - The x and y -values (in the plot's scale) will be saved in datax and datay.")
print(r'   - The marker colour is saved in variable c, so to change the marker color, use e.g. c=\'b\.\n')
print('  show_data(): print datax and datay')
print('  rmlast()   : remove last inserted value')
print('  clear()    : Clear datax and datay')

change_size = False
if pix: points = ax.scatter([],[],color=c, marker='+')

def clear():
    global datax,datay,pointsx,pointsy,dx,dy,lengths,colors
    datax = []
    datay = []
    pointsx = []
    pointsy = []
    dx = []
    dy = []
    lengths = []
    colors = []
    dx0 = None
    dy0 = None
    if pix: points.set_offsets(np.array([pointsx,pointsy]).T)


def rmlast():
    global datax,datay,last,pointsx,pointsy,dx,dy,lengths
    datax.pop(-1)
    datay.pop(-1)
    pointsx.pop(-1)
    pointsy.pop(-1)
    dx.pop(-1)
    dy.pop(-1)
    lengths.pop(-1)
    if not pix: last.remove()
    if pix: points.set_offsets(np.array([pointsx,pointsy]).T)

def show_data():
    print('x           y')
    for i in range(len(datax)):
        print(datax[i], datay[i])

def show_lengths():
    print('dx           dy           lengths')
    for i in range(len(dx)):
        print(f'{dx[i]:12.6f} {dy[i]:12.6f} {lengths[i]:12.6f}')

def show_colors():
    for i in range(len(colors)):
        print(f'({colors[i][0]:6.3f},{colors[i][1]:6.3f},{colors[i][2]:6.3f})')



#
