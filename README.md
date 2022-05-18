# **ByzMT Parsed Version Format into OSHB JSON Format**

This tool will take the parsed format of Byzantine Majority Text (ByzMT) by
Robinson-Pierpoint, then change the format into the Open Scripture's Hebrew
Bible (OSHB) JSON format.

Tools for parsing OSHB JSON format into OSHB XML format is available on [their
repository](https://github.com/openscriptures/morphhb), so the product of this
tool could be later used as an XML too.)

## **Goal**

To make available the ByzMT for other tools that can parse the OSHB JSON format.

## **Usage**

Simply `./run.sh`.

## **Source**

This tool is basically a trimmed and modified version of
[librobinson](https://github.com/byztxt/librobinson) with extra script.

## **License**

Everything is licensed with MIT except for `./modified-librobinson/convert.py`.
