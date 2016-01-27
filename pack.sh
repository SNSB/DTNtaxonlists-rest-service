#!/bin/bash
git diff-index --quiet HEAD && echo "$(git log | grep commit | wc -l)" > static/revision.txt || echo  "$(( $(git log | grep commit | wc -l) + 1 ))" > static/revision.txt
pip freeze > requirements.tmp
[[ $( diff requirements.txt requirements.tmp ) ]] && mv requirements.{tmp,txt}
rm requirements.tmp
./makefilelist
[[ $( diff filelist.txt filelist.tmp ) ]] && mv filelist.{tmp,txt}
rm filelist.tmp
rm restnames.tar
tar -c -h -v -T filelist.txt -f restnames.tar
