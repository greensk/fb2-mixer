#!/usr/bin/python3
# Copyright (C) 2017 Grigory Kosheev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import glob
import datetime

from list import BooksList
from item import BookItem


inputDir = sys.argv[1]
outputDir = sys.argv[2]

params = {'shuffle': True, 'clean': True, 'appendBookData': True, 'zipOutput': True, 'flushMetaData': True, 'expand': True, 'cleanHead': True}
bulkName = datetime.datetime.now().strftime('%y%m%d')

booksList = BooksList(inputDir)

if params['shuffle']:
    booksList.shuffle()
    
num = 1

for bookFilePath in booksList.books:
    bookObject = BookItem(bookFilePath)

    fileTitle = '%s-%04d' % (bulkName, num)
    
    if params['clean']:
        bookObject.clean()

    if params['appendBookData']:
        bookObject.appendBookData()

    if params['cleanHead']:
        bookObject.cleanHead()

    if params['flushMetaData']:
        bookObject.flushMetaData(fileTitle)


    if params['expand']:
        bookObject.expand()
    
    outputFilename = '%s/%s.fb2' % (outputDir, fileTitle)
    bookObject.output(outputFilename, params['zipOutput'])

    num += 1

