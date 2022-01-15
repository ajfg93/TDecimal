#!/usr/bin/env bash

coverage run -m unittest TDecimalUnitTest.py && coverage report -m && coverage html

