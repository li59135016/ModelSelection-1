from datetime import datetime
from ModelSelection import LinearRegression
from Hypotheses import *
from Plots import *
import matplotlib.pyplot as pl
import time

def test_generator(generator):
    """ Plot randomly generated data.
    :param generator: Hypothesis to use.
    """
    assert isinstance(generator, Hypothesis)
    xx = np.array(np.arange(-1.0, 3.0, step=0.04))
    tt = generator.generate(xx)

    pl.plot(xx, tt, 'ro')
    pl.show()


def select_points_and_fit(regression, num=10):
    """ Opens an interactive window to draw points

    :param num: expected number of points
    :type regression: LinearRegression
    """
    assert isinstance(regression, LinearRegression)

    pl.ion()
    fig, (ax1, ax2) = pl.subplots(2)
    ax1.set_xlim((-10, 10))  # FIXME!!! ranges in (-1,1) won't work???
    ax1.set_ylim((-10, 10))
    points = fig.ginput(n=num, timeout=0)
    if len(points) == 0:
        return
    pl.ioff()

    dt = datetime.now()
    for p in points:
        # print ("Updating with (%f, %f)" % (p[0], p[1]))
        regression.update(p[0], p[1])
    dt = datetime.now() - dt
    msec = (dt.days * 24 * 3600 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    print "Update completed in %d milliseconds." % msec

    wmap = [param.mean for param in regression.parameter]

    updateMAPFitPlot(ax1, regression.XHist, regression.hypotheses, wmap, 0.05)
    pl.draw()
    ax1.plot(regression.XHist, regression.THist, 'ro')
    pl.draw()
    updateProbabilitiesPlot(ax2, regression)
    pl.draw()
    pl.show(block=True)

def select_points_and_fit_interactive(regression):
    """ Opens an interactive window to draw points

    :param num: expected number of points
    :type regression: LinearRegression
    """
    assert isinstance(regression, LinearRegression)

    fig, (ax1, ax2) = pl.subplots(2)
    ax1.set_xlim((0, 3))  # FIXME!!! ranges in (-1,1) won't work???
    ax1.set_ylim((-4, 4))
    pid = []
    for n in range(1, 40):
        pl.ion()
        points = fig.ginput(n=1, timeout=0)
        p = points[0]
        if len(points) == 0:
            return
        pl.ioff()

        dt = datetime.now()
        # print ("Updating with (%f, %f)" % (p[0], p[1]))
        regression.update(p[0], p[1])
        dt = datetime.now() - dt
        msec = (dt.days * 24 * 3600 + dt.seconds) * 1000 + dt.microseconds / 1000.0
        print "Update completed in %d milliseconds." % msec

        wmap = [param.mean for param in regression.parameter]
        ax1.cla()
        ax1.set_xlim((0, 3))  # FIXME!!! ranges in (-1,1) won't work???
        ax1.set_ylim((-4, 4))
        updateMAPFitPlot(ax1, regression.XHist, regression.hypotheses, wmap, 0.005)
        ax1.plot(regression.XHist, regression.THist, 'ro')
        pl.draw()
        ax2.cla()
        updateProbabilitiesPlot(ax2, regression)
        pl.draw()
        continue
        pl.show()

def generate_noise_and_fit_iterative(regression, generator, xmin=0.0, xmax=3.0, num=10):
    """
    Generate data (input) points in the specified range and use the generator Hypothesis $y$ to
    synthesize target (output) values $t$ according to the formula

      $t = y (x, w) + \epsilon$

    where $\epsilon$ is the noise associated to the generator.

    Then apply the regression to these target values.

    :type regression: LinearRegression
    :type generator: Hypothesis.*
    """
    assert isinstance(regression, LinearRegression)
    assert isinstance(generator, Hypothesis)

    inputs = np.array(np.arange(xmin, xmax, step=(float(xmax)-float(xmin))/float(num)))
    #dt = datetime.now()
    fig, (ax1, ax2) = pl.subplots(2)
    gen_values = generator.generate(inputs)
    ymin = min(gen_values)
    ymax = max(gen_values)
    pl.show(block=False)
        
    for x, t in zip(inputs, gen_values):
        ax1.cla()
        ax2.cla()
        # print ("Updating with (%f, %f)" % (x, t))
        regression.update(x, t)

        #dt = datetime.now() - dt
        #msec = (dt.days * 24 * 3600 + dt.seconds) * 1000 + dt.microseconds / 1000.0
        #print "Update completed in %d milliseconds." % msec

        wmap = [param.mean for param in regression.parameter]

        # Plot
        updateMAPFitPlot(ax1, regression.XHist, regression.hypotheses, wmap, 0.005)
        ax1.set_xlim((xmin, xmax))
        ax1.set_ylim((ymin, ymax))
        pl.draw()
        ax1.plot(regression.XHist, regression.THist, 'ro')
        pl.draw()
        updateProbabilitiesPlot(ax2, regression)
        pl.draw()
        time.sleep(.3)


def generate_noise_and_fit(regression, generator, xmin=0.0, xmax=1.0, num=10):
    """
    Generate data (input) points in the specified range and use the generator Hypothesis $y$ to
    synthesize target (output) values $t$ according to the formula

      $t = y (x, w) + \epsilon$

    where $\epsilon$ is the noise associated to the generator.

    Then apply the regression to these target values.

    :type regression: LinearRegression
    :type generator: Hypothesis.*
    """
    assert isinstance(regression, LinearRegression)
    assert isinstance(generator, Hypothesis)

    inputs = np.array(np.arange(xmin, xmax, step=(float(xmax)-float(xmin))/float(num)))
    dt = datetime.now()
    gen_values = generator.generate(inputs)
    ymin = min(gen_values)
    ymax = max(gen_values)
    for x, t in zip(inputs, gen_values):
        # print ("Updating with (%f, %f)" % (x, t))
        regression.update(x, t)

    dt = datetime.now() - dt
    msec = (dt.days * 24 * 3600 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    print "Update completed in %d milliseconds." % msec

    wmap = [param.mean for param in regression.parameter]

    # Plot
    fig, (ax1, ax2) = pl.subplots(2)
    updateMAPFitPlot(ax1, regression.XHist, regression.hypotheses, wmap, 0.005)
    pl.draw()
    ax1.plot(regression.XHist, regression.THist, 'ro')
    pl.draw()
    updateProbabilitiesPlot(ax2, regression)
    pl.draw()
    pl.show(block=True)


##############################################################################
# FIXME: cannot use multiple windows / figures
##############################################################################

hc = HypothesisCollection()
hc.append(PolynomialHypothesis(M=2, variance=16))
hc.append(PolynomialHypothesis(M=3, variance=16))
hc.append(PolynomialHypothesis(M=4, variance=16))
hc.append(PolynomialHypothesis(M=8, variance=16))
hc.append(TrigonometricHypothesis(halfM=10, variance=16))

obsNoiseSigma = 0.2 #try 0.2 for Polynomials
lr = LinearRegression(hc, obsNoiseSigma)
#select_points_and_fit_interactive(lr)
#select_points_and_fit(lr, num=2)
#generate_noise_and_fit(lr, generator=PolynomialHypothesis(M=3, variance=1), xmin=0, xmax=3, num=50)
#generate_noise_and_fit_iterative(lr, generator=PolynomialHypothesis(M=4, variance=0.2), xmin=0, xmax=4, num=30)
generate_noise_and_fit_iterative(lr, generator=PolynomialHypothesis(M=3, variance=4, noiseVariance=obsNoiseSigma**2), xmin=0, xmax=3, num=50)
#generate_noise_and_fit_iterative(lr, generator=TrigonometricHypothesis(halfM=6, variance=1), xmin=0, xmax=3*math.pi, num=30)
input()

"""
lr.update(0, 1.5)
lr.update(0.5, 0.75)
lr.update(1, 0)
lr.update(2, -3)
lr.update(3, -8)
wmap = [param.mean for param in lr.parameter]
pl.clf()
getMAPFitPlot(lr.XHist, hc, wmap, 0.05)
pl.plot(lr.XHist, lr.THist, 'ro')
pl.show()
pl.clf()
getProbabilitiesPlot(lr)
pl.show()

"""

"""
fig = pl.figure()
ax = fig.add_subplot(111, xlim=(-2, 2), ylim=(-2, 2))
def on_click(event):
    print ("X=%f, Y=%f" % (event.x, event.y))
    fig.gca().scatter(event.x, event.y)
    fig.canvas.draw()

# bind pick events to our on_pick function
fig.canvas.mpl_connect('button_press_event', on_click)
pl.show()
"""
