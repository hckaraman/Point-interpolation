# Python bytecode 3.7 (3394)
# Embedded file name: C:\Users\cagri\PycharmProjects\Monte_Carlo\iter\inter1.py
# Size of source mod 2**32: 4643 bytes
import numpy as np
import matplotlib.pyplot as plt
import os, csv, pandas as pd
from appJar import gui
from pathlib import Path


def iter(input_file, out_file, points,plot):
    Ets = []
    Ett = []
    points = int(points)
    try:
        with open(input_file) as (csvDataFile):
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                Ets.append(float(row[0]))
                Ett.append(float(row[1]))

    except:
        print('Data file could not read')

    Ets = np.array(Ets)
    Ett = np.array(Ett)
    c = np.linspace(np.min(Ets), np.max(Ets), int(points))
    r = np.zeros(len(c))
    x = np.zeros(2)
    y = np.zeros(2)
    new = []
    it = np.zeros(10)
    for i in range(len(Ets) - 1):
        it = np.linspace(Ets[i], Ets[i + 1], 10)
        new.append(it)

    for i in range(len(Ets)-1):
        x[0] = Ets[i]
        x[1] = Ets[i + 1]
        y[0] = Ett[i]
        y[1] = Ett[i + 1]
        fit = np.polyfit(x, y, 1)
        fit_fn = np.poly1d(fit)
        for j in range(len(c)):
            if c[j] >= Ets[i] and c[j] <= Ets[i + 1] or c[j] <= Ets[i] and c[j] >= Ets[i + 1]:
                r[j] = fit_fn(c[j])
    # c = np.delete(c, -1)
    # r = np.delete(r, -1)
    f = open(out_file, 'w')
    # f.write('Reg_X Reg_Y\n')
    np.savetxt(out_file, np.c_[(c, r)], delimiter=',',fmt = '%10.4f,%10.4f')
    # np.savetxt(out_file, np.c_[(c, r)],delimiter=',')

    if plot==True:
        r[len(c) - 1] = Ett[len(Ett) - 1]

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(111)
        ax.set_title('Interpolation on stations')
        ax.set_xlabel('Station (m)')
        ax.set_ylabel('Elevation (m) ')
        ax.plot(Ets, Ett, 's-', c, r, 'o--')
        plt.gca().legend(('Original Values', 'Interpolated Values'))
        plt.show()

    print('Calculation finished. Check %s file' % out_file)


def press(button):
    """ Process a button press

    Args:
        button: The name of the button. Either Process of Quit
    """
    if button == 'Process':
        src_file = app.getEntry('Input_File')
        dest_dir = app.getEntry('Output_Directory')
        out_file = app.getEntry('Output_name')
        points = app.getEntry('Points')
        out_file = out_file + '.csv'
        plot = app.getCheckBox('Plot Results')
        iter(src_file, Path(dest_dir, out_file), points,plot)
    else:
        app.stop()

app = gui('interpolate', useTtk=True)
app.setTtkTheme('default')
app.setSize(500, 200)
app.addLabel('Choose Source PDF File')
app.addFileEntry('Input_File')
app.addLabel('Select Output Directory')
app.addDirectoryEntry('Output_Directory')
app.addLabel('Output file name')
app.addEntry('Output_name')
app.addLabel('Number of Points')
app.addEntry('Points')
app.addCheckBox("Plot Results")

app.addButtons(['Process', 'Quit'], press)
app.go()