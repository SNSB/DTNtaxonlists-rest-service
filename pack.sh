#!/bin/bash
pip freeze > requirements.txt
./makefilelist
tar -c -h -v -T filelist.txt -f restnames.tar
