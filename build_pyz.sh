#!/bin/sh -x
if [ -z "$1" ];then
  echo 'Must set .pyz as first argument'
  exit 1
fi
set -e
source_file=`readlink -f $0`
source_folder=`dirname $source_file`
pyz_path=`readlink -f $1`
rm -i $pyz_path || true
(cd $source_folder && zip -r $pyz_path *.py static_files)
