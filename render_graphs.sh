#!/bin/bash

eval mkdir -p graphs

eval dot -Tpng friends_graph_no_clusters.dot > graphs/friends_graph_no_clusters_dot.png
eval dot -Tpdf friends_graph_no_clusters.dot > graphs/friends_graph_no_clusters_dot.pdf
eval fdp -Tpng friends_graph_no_clusters.dot > graphs/friends_graph_no_clusters_fdp.png
eval fdp -Tpdf friends_graph_no_clusters.dot > graphs/friends_graph_no_clusters_fdp.pdf

eval fdp -Tpng friends_graph_clusters.dot > graphs/friends_graph_clusters.png
eval fdp -Tpdf friends_graph_clusters.dot > graphs/friends_graph_clusters.pdf
