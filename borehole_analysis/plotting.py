#!/usr/bin/env python
""" file:   plotting.py (borehole_analysis)
    author: Jess Robertson
            CSIRO Earth Science and Resource Engineering
    email:  jesse.robertson@csiro.au
    date:   Wednesday May 1, 2013

    description: Plotting for the borehole_analysis module.
"""

import matplotlib.pyplot
import matplotlib.cm
import matplotlib.collections
import numpy
import sklearn.manifold
from borehole_analysis.analyser import AnalystError

def make_figure_grid(nplots, ncols=3, size=6):
    """ Make a grid of images
    """
    nrows = nplots / ncols
    if nrows * ncols != nplots:
        nrows += 1
    fig = matplotlib.pyplot.figure(figsize=(ncols * size, nrows * size))
    axeses = [matplotlib.pyplot.subplot(nrows, ncols, i+1)
              for i in range(nplots)]
    return fig, axeses

def plot_variable(axes, variable, cmap=None):
    """ Generate a single image of a wavelet transform
    """
    if cmap is None:
        cmap = matplotlib.cm.get_cmap('Paired')
    axes.imshow(variable.T, cmap=cmap, interpolation='nearest')
    axes.set_aspect(variable.shape[0] / float(variable.shape[1]))
    axes.set_xlabel(r"Fourier Scale $\lambda_{i}$")
    axes.set_xticklabels([''])
    axes.set_xticks([])
    axes.set_ylabel(r"Domain $x_{i}$")
    axes.set_yticklabels([''])
    axes.set_yticks([])

def plot_difference(axes, domain, observed_value, expected_value,
    colors=('red', 'blue'), orientation='horizontal'):
    """ Plots the difference between two series.

        This plot also includes a set of lines in the shading to indicate the sample spacing. You can set the colors that you want to use to highlight differences between the two series.

        :param axee: The axes to plot in
        :type axes: `matplotlib.pyplot.axes`
        :param domain: The domain variable
        :type domain: `numpy.ndarray`
        :param observed_value: The actual value given as a numpy array. Must be the same length as the domain vector.
        :type observed_value: `numpy.ndarray`
        :param expected_value: The expected value. Can be a constant, in which case the value will be constant, or an array of the same size as the domain.
        :type expected_value: `numpy.ndarray` or number
        :param colors: A tuple of colors. The fill and lines will be shaded `color[0]` when `observed_value` < `expected_value` and `color[1]` when `observed_value` >= `expected_value`. Any color accepted by matplotlib is allowed.
        :type colors: Tuple
        :param orientation: The orientation of the plot, one of 'horizontal', or 'vertical'.
        :type orientation: str
    """
    # Expand the expected value if required
    if type(expected_value) is not numpy.ndarray:
        expected_value = expected_value * numpy.ones_like(domain)

    # Helper functions for plotting the lines
    pos_diff = lambda a, b: a + numpy.maximum(b-a, 0)
    neg_diff = lambda a, b: a + numpy.minimum(b-a, 0)

    # Generate plot
    if orientation is 'horizontal':
        # Plot the two signals
        axes.plot(domain, observed_value, color='black', linewidth=1)
        axes.plot(domain, expected_value, 'k--', linewidth=1)

        # Generate fills
        axes.vlines(domain, expected_value,
            pos_diff(expected_value, observed_value), color=colors[1])
        axes.vlines(domain, neg_diff(expected_value, observed_value),
            expected_value, color=colors[0])
        axes.fill_between(domain, expected_value, observed_value,
            where=(observed_value >= expected_value),
            alpha=0.1, facecolor=colors[1])
        axes.fill_between(domain, expected_value, observed_value,
            where=(observed_value <  expected_value),
            alpha=0.1, facecolor=colors[0])
    elif orientation is 'vertical':
        # Plot the two signals
        axes.plot(observed_value, domain, color='black', linewidth=2)
        axes.plot(expected_value, domain, 'k--', linewidth=2)

        # Generate fills
        axes.hlines(domain, expected_value,
            pos_diff(expected_value, observed_value), color=colors[1])
        axes.hlines(domain, neg_diff(expected_value, observed_value),
            expected_value, color=colors[0])
        axes.fill_betweenx(domain, expected_value, observed_value,
            where=(observed_value >= expected_value),
            alpha=0.1, facecolor=colors[1])
        axes.fill_betweenx(domain, expected_value, observed_value,
            where=(observed_value <  expected_value),
            alpha=0.1, facecolor=colors[0])
    else:
        raise ValueError('Argument `orientation` must be "horizontal" or '
            'vertical"')

def plot_signal(axes, domain, signal, orientation='horizontal'):
    """ Plots a one-dimensional signal against some domain.

        This assumes that you're plotting a detrended signal, so it fills in red for negative anomalies and blue for positive anomalies, so that you can compare the deviation from the trend.

        :param axes: The axes instance in which to plot the signal
        :type axes: `matplotlib.axes`
        :param domain: An array of domain locations
        :type domain: `numpy.ndarray`
        :param signal: An array of signal values. Must be the same length as `domain` or an error will be raised.
        :type signal: `numpy.ndarray`
        :param orientation: One of `'horizontal'` or `'vertical'`
        :type orientation: `str`
    """
    # Generate plot
    plot_difference(axes, domain, signal, signal.mean(),
        colors=('red', 'blue'),
        orientation=orientation)
    if orientation is 'horizontal':
        axes.set_xlabel('Domain $x$')
        axes.set_ylabel(r'Signal $f(x)$',
            rotation=0,
            horizontalalignment='right',
            verticalalignment='center')
        axes.set_xlim(domain[0], domain[-1])
        axes.set_ylim(numpy.min(signal), numpy.max(signal))
    elif orientation is 'vertical':
        axes.set_ylabel('Domain $x$')
        axes.set_xlabel('Signal $f(x)$')
        axes.set_xlim(numpy.min(signal), numpy.max(signal))
        axes.set_ylim(domain[-1], domain[0])
    else:
        raise ValueError('Argument `orientation` must be "horizontal" or '
            'vertical"')

def plot_connection_graph(embedding, correlations, names, cluster_labels):
    """ Plots a connection graph in 2D given an embedding and a correlation
        matrix.
    """
    # Plot the nodes using the coordinates of our embedding
    axes = matplotlib.pyplot.gca()
    axes.scatter(embedding[0], embedding[1],
        c=cluster_labels,
        cmap=matplotlib.cm.get_cmap('Spectral'))

    # Plot the edges - a sequence of (*line0*, *line1*, *line2*), where
    #            linen = (x0, y0), (x1, y1), ... (xm, ym)
    non_zero = numpy.logical_not(correlations.mask)
    start_idx, end_idx = numpy.where(non_zero)
    segments = [[embedding[:, start], embedding[:, stop]]
                for start, stop in zip(start_idx, end_idx)]
    values = correlations[non_zero]
    lines = matplotlib.collections.LineCollection(segments,
        zorder=0,
        cmap=matplotlib.cm.get_cmap('RdBu'),
        norm=matplotlib.pylab.Normalize(.7 * values.min(), .7 * values.max()))
    lines.set_array(values)
    lines.set_linewidths(15 * numpy.abs(values))
    axes.add_collection(lines)

    # Add a label to each node
    label_info = zip(names, cluster_labels, embedding.T)
    for index, (name, label, (xloc, yloc)) in enumerate(label_info):
        (xloc, yloc), alignment = float_label(index, (xloc, yloc), embedding)
        point_color = matplotlib.cm.get_cmap('Spectral')(
            label / float(max(cluster_labels)))
        matplotlib.pylab.text(xloc, yloc, name, size=10,
                horizontalalignment=alignment[0],
                verticalalignment=alignment[1],
                bbox=dict(facecolor=point_color,
                          edgecolor=point_color,
                          alpha=.3))

    # Adjust axes limits
    axes.set_xlim(embedding[0].min() - .15 * embedding[0].ptp(),
            embedding[0].max() + .10 * embedding[0].ptp(),)
    axes.set_ylim(embedding[1].min() - .03 * embedding[1].ptp(),
            embedding[1].max() + .03 * embedding[1].ptp())

def float_label(index, position, embedding):
    """ Floating labels for plot so that they avoid one another.

        The challenge here is that we want to position the labels to avoid
        overlap with other labels. We use the neighbour data in the embedding
        to juggle the label positions to avoid collisions.
    """
    xloc, yloc = position
    dxloc = xloc - embedding[0]
    dxloc[index] = 1
    dyloc = yloc - embedding[1]
    dyloc[index] = 1
    this_dxloc = dxloc[numpy.argmin(numpy.abs(dyloc))]
    this_dyloc = dyloc[numpy.argmin(numpy.abs(dxloc))]
    if this_dxloc > 0:
        horizontalalignment = 'left'
        xloc += .002
        yloc += .001
    else:
        horizontalalignment = 'right'
        xloc -= .002
        yloc -= .001
    if this_dyloc > 0:
        verticalalignment = 'bottom'
        yloc += .002
        xloc += .001
    else:
        verticalalignment = 'top'
        yloc -= .002
        xloc -= .001

    return (xloc, yloc), (horizontalalignment, verticalalignment)

## Borehole plotting
def plot_borehole_data(borehole, keys_to_plot=None):
    """ Plot the data stored in the current node object

        :returns: handles to the figure and axes
    """
    if keys_to_plot is None:
        keys_to_plot = borehole.get_keys()

    # Get data from borehole
    domain = borehole.get_domain()
    signals = dict([(k, borehole.get_signal(k)) for k in keys_to_plot])
    domain_bounds = (borehole.domain.min(), borehole.domain.max())

    # Plot data
    fig = matplotlib.pyplot.figure(figsize=(1*len(keys_to_plot), 20))
    for i, key in enumerate(keys_to_plot):
        axes = matplotlib.pyplot.subplot(1, len(keys_to_plot), i+1)
        plot_signal(axes, signal=signals[key], domain=domain,
            orientation='vertical')
        axes.set_xlabel("")
        if i == 0:
            axes.set_ylabel('Depth (m)')
        else:
            axes.set_ylabel("")
            axes.set_yticklabels("")
        axes.set_ylim(domain_bounds)
        axes.xaxis.set_major_locator(matplotlib.pyplot.MaxNLocator(3))
        axes.set_title(borehole.labels[key][1],
            rotation=90, verticalalignment='bottom',
            horizontalalignment='center')
    fig.tight_layout()
    return fig, axes


## Analyst plotting
def plot_eigensignals(node):
    """ Plot the eigensignal axes for the current data
    """
    # Get clusters from current node
    clusters = node.products['clusters']['by_key']
    cluster_sources = node.products['eigensignals']
    domain = node.get_domain()

    # Plot eigensignals for node
    data = zip(clusters.items(), cluster_sources)
    for (cluster_index, cluster_keys), sources in data:
        fig = matplotlib.pyplot.figure(figsize=(10, 2*len(sources)))
        for index, source in enumerate(sources):
            axes = matplotlib.pyplot.subplot(len(sources), 1, index+1)
            plot_signal(axes,
                domain=domain,
                signal=source,
                orientation='horizontal')
            axes.set_ylabel(r'$S_{{{0}, {1}}}(x)$'.format(cluster_index,
                index))
            if index == 0:
                axes.set_title('Cluster {0}: {1}'.format(cluster_index,
                    ', '.join(cluster_keys)))
            if index == len(sources) - 1:
                axes.set_xlabel(r'Depth $x$ (m)')
            else:
                axes.set_xlabel('')
                axes.set_xticklabels('')
        fig.tight_layout()

def plot_cusum(node, *keys):
    """ Plot the CUSUM for the given keys.
    """
    fig = matplotlib.pyplot.figure(figsize=(5, 8))
    axes = fig.gca()
    for key in keys:
        # Generate cusum
        signal = node.get_signal(key)
        cusum = numpy.cumsum((signal - signal.mean()) / signal.std())

        # Renormalise to lie between [0, 1]
        maxsum, minsum = cusum.max(), cusum.min()
        cusum -= minsum
        cusum /= maxsum - minsum

        # Plot it
        axes.plot(cusum, node.domain,
            label=node.labels[key][1],
            linewidth=2)
    axes.set_ylim(node.domain[-1], node.domain[0])
    axes.legend(loc='upper left', bbox_to_anchor=(1, 1))
    fig.tight_layout()
    return fig, axes

def plot_connection_matrix(node):
    """ Plots the connection matrix assicated with the data in the current
        node.

        :returns: handles to the figure and axes
    """
    # Calculate correlation matrix
    names = node.borehole.get_labels()
    correlations = node.products['correlations']

    # Plot results
    side_len = 0.5*len(names)
    fig = matplotlib.pyplot.figure(figsize=(side_len, side_len))
    axes = matplotlib.pyplot.gca()
    image = axes.imshow(correlations,
        interpolation='none',
        cmap=matplotlib.cm.get_cmap("RdBu_r"))
    cbar = matplotlib.pyplot.colorbar(image,
        fraction=0.2,
        shrink=(1 - 0.25))
    cbar.set_label('Correlation')
    axes.set_xticks(range(len(names)))
    axes.set_xticklabels(names, rotation=90,
        horizontalalignment='center',
        verticalalignment='top')
    axes.set_yticks(range(len(names)))
    axes.set_yticklabels(names)
    return fig, axes

def plot_node_connection_graph(node, embedding=None):
    """ Plot the clusters and connections between data signals.

        We use manifold learning methods to find a low-dimension embedding
        for visualisation. For the methods here we use a dense eigensolver
        to achieve reproducibility (since arpack is initialised with
        random vectors - the result would be different each time) In
        addition, we use a large number of neighbours to capture the large-
        scale structure.

        This could potentially be sped up significantly by using a sparse
        representation, at the cost of introducing some randomness to the
        visualisation.

        :param embedding: The model to use to embed the nodes in two-dimensional space. If None, it defaults to 'isomap'.
        :type embedding: `'lle'` or `'isomap'`
        :returns: handles to the figure and axes
    """
    # Get node infomation
    names = node.borehole.get_labels()
    clusters = node.products['clusters']['as_vector']

    # Calculate embedding
    embedding = embedding or 'isomap'
    if embedding is 'isomap':
        node_position_model = sklearn.manifold.Isomap(
            n_components=2,
            eigen_solver='dense',
            n_neighbors=len(names) - 2)
    elif embedding is 'lle':
        node_position_model = sklearn.manifold.LocallyLinearEmbedding(
            n_components=2,
            eigen_solver='dense',
            n_neighbors=len(names) - 2)
    else:
        raise AnalystError("Embedding argument to plot_connection_graph"
            "must be one of 'lle' or 'isomap'")
    embedding = node_position_model.fit_transform(node.data.T).T

    # Plot results
    fig = matplotlib.pyplot.figure(figsize=(15, 15))
    plot_connection_graph(
        names=names,
        cluster_labels=clusters,
        embedding=embedding,
        correlations=node.products['correlations'])
    axes = matplotlib.pyplot.gca()
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)
    axes.set_title('Network graph')
    return fig, axes