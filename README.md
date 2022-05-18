# **ByzMT Parsed to OSHB JSON Converter**

This tool will take the [parsed
version](https://github.com/byztxt/byzantine-majority-text/tree/master/parsed)
of the [Byzantine Majority Text by Robinson-Pierpoint
(ByzMT)](https://github.com/byztxt/byzantine-majority-text) and converts the
format into the [Open Scripture's Hebrew Bible (OSHB) JSON
format](https://github.com/benihyangbaik/interlinear-bible-simple-editor/blob/main/data/morphhb.json).

Tools for parsing OSHB JSON format into OSHB XML format is available on [their
repository](https://github.com/openscriptures/morphhb), so the product of this
converter could be later used as an XML too.)

## **Goal**

To make available the ByzMT for other tools that can parse the OSHB JSON format.

## **Usage**

Simply `./run.sh`.

## **Source**

This tool is basically a trimmed and modified version of
[librobinson](https://github.com/byztxt/librobinson) with extra script.

## **License**

Everything is licensed with MIT except for `./modified-librobinson/convert.py`.
