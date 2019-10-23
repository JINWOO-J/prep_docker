#!/bin/sh
today=$(date +"%Y-%m-%d %T")
cp README_HEADER.md README_HEADER_TMP.md
for image in prep-node
do
    echo "## $image docker setting" >README_TAIL.md
    echo "###### made date at $today " >>README_TAIL.md
    cat src/entrypoint.sh  | grep ^export | grep -v except| cut -d "=" -f1 | sed 's/export//g' | sed 's/_/\\_/g' | sed -e 's/^/\|/' > text1
    cat src/entrypoint.sh | grep ^export | grep -v except | cut -d "-" -f2- | cut -d "#" -f1 | sed 's/ *$//'| sed -E 's/-$|}$|"//g'  |  sed 's/_/\\_/g' > text2
    cat src/entrypoint.sh | grep ^export | grep -v except| cut -d "-" -f2- | cut -d "#" -f2 | sed 's/ *$//'| sed -E 's/-$|}$|"//g'  | sed 's/_/\\_/g'  > text3
    cat src/entrypoint.sh | grep ^export | grep -v except| cut -d "-" -f2- |  awk -F"#" '{print $3}'|sed -E 's/-$|}$|"//g'  | sed 's/_/\\_/g'| sed 's/\|/\\|/'| sed -e 's/$/\|/' > text4
    echo "| Environment variable | Description|Default value| Allowed value|" >>README_TAIL.md
    echo "|--------|--------|-------|-------|"     >>README_TAIL.md
    paste -d "|" text1  text3 text2  text4      >>README_TAIL.md
done

cat README_HEADER_TMP.md  > README.md
echo "" >> README.md
cat README_TAIL.md  >> README.md

rm -f text1 text2 text3 text4 README_HEADER_TMP.md README_TAIL.md