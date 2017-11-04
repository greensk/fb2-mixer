#!/usr/bin/python3

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

