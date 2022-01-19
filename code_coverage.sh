#!/usr/bin/env bash

if [[ "$1" == "no-html-gen" ]];
then
  coverage run -m unittest TDecimalUnitTest.py && coverage report -m
else
  coverage run -m unittest TDecimalUnitTest.py && coverage report -m && coverage html
fi

