#!/bin/bash
pip freeze > requirements.txt
./makefilelist
rm restnames.tar
tar -c -h -v -T filelist.txt -f restnames.tar
