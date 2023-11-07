#!/bin/sh

db=`grep db: config/config.yaml |sed -e 's#.*:\(\)#\1#'`