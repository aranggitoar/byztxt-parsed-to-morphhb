# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Benih Yang Baik
#
# Made available under the MIT License.
#
# See the file LICENSE in the distribution for details.
#

#!/bin/bash


# -------
echo $'\n> Get the byztxt parsed version.\n'

# Prepare the environment
rm -rf s src outdir
mkdir outdir

# Clone an empty and shallow repo
git clone --depth=1 --filter=blob:none --sparse \
  https://github.com/byztxt/byzantine-majority-text s

# Checkout only the parsed directory
cd s
git sparse-checkout init --cone
git sparse-checkout set parsed

# Move the whole directory
mv parsed ../src

# Remove the partially cloned repo
cd ..
rm -rf s


# -------
echo $'\n> Format byztxt parsed version into morphhb.\n'

# Run the modified librobinson
python2 ./modified-librobinson/robinson.py


# -------
echo $'\n> Cleaning source tree, check ./outdir/byzparsed.json.\n'

# Clean the environment
rm -rf src
