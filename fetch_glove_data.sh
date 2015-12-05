#!/bin/bash

url=http://nlp.stanford.edu/data/glove.6B.zip
fname=`basename $url`

wget $url
mv $fname data/glove
unzip data/glove/$fname -d data/glove/

