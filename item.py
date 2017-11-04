from lxml import etree
from zipfile import ZipFile
import ntpath
import random

parser = etree.XMLParser(recover=True)
namespaces = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}

class BookItem:
    def __init__(self, path):
        self.path = path
        self._xml = None
        if path.endswith('.fb2.zip'):
            self.zip = True
        else:
            self.zip = False
    def output(self, filename):
        pass
    def getFileContent(self):
        if (self.zip):
            zip = ZipFile(self.path, 'r')
            contentFile = ntpath.basename(self.path).replace('.zip', '')
            content = zip.read(contentFile)
            zip.close()
            return content
        else:
            return open(self.path, 'rb').read()
            
    def getTagContent(self, tag):
        xml = self.getXmlContent()
        if xml != None:
            # print(etree.tostring(xml, pretty_print=True))
            elements = xml.xpath('//fb:%s' % tag, namespaces=namespaces)
            if len(elements) > 0:
                return elements[0].text
        return None

    def getBookData(self, includeFilename = True):
        data = {}
        data['Название'] = self.getTagContent('book-title')
        data['Автор'] = '%s %s' % (self.getTagContent('first-name'), self.getTagContent('last-name'))
        if includeFilename:
            data['Имя файла'] = ntpath.basename(self.path)
        return data

    def getXmlContent(self):
        if self._xml != None:
            return self._xml
        fileContent = self.getFileContent()
        if fileContent:
            self._xml = etree.fromstring(fileContent, parser)
            return self._xml
        else:
            return None
            
    def clean(self):
        xml = self.getXmlContent()
        for bad in xml.xpath('//fb:title', namespaces=namespaces):
            bad.getparent().remove(bad)

    def appendBookData(self):
        info = self.getBookData()
        xml = self.getXmlContent()
        body = xml.xpath('//fb:body', namespaces=namespaces)[0]
        strings = ['', 'Вы читали:']
        for param in info:
            strings.append('%s: %s' % (param, info[param]))
        for str in strings:
            newElement = etree.SubElement(body, 'p')
            newElement.text = str

    def flushMetaData(self, fileTitle):
        self.flushTag('//fb:book-title', fileTitle)
        self.flushTag('//fb:author/fb:first-name')
        self.flushTag('//fb:author/fb:last-name')
        self.flushTag('//fb:author/fb:middle-name')
        self.flushTag('//fb:genre')
        self.removeTag('//fb:annotation')
        self.removeTag('//fb:image')
        self.removeTag('//fb:epigraph')

    def flushTag(self, xpath, content = ''):
        xml = self.getXmlContent()
        for element in xml.xpath(xpath, namespaces=namespaces):
            element.text = content

    def removeTag(self, xpath):
        xml = self.getXmlContent()
        for element in xml.xpath(xpath, namespaces=namespaces):
            element.getparent().remove(element)

    def expand(self):
        number = random.randint(1000, 10000)
        for x in range(0, number):
            self.addEmptyString()

    def addEmptyString(self):
        xml = self.getXmlContent()
        body = xml.xpath('//fb:body', namespaces=namespaces)[0]
        newElement = etree.SubElement(body, 'p')
        newElement.text = 'X' * 1000

    def cleanHead(self):
        maxLines = 10 # max head lines
        xml = self.getXmlContent()
        headLines = xml.xpath('//fb:body//fb:p', namespaces=namespaces)

        dataToRemove = list(self.getBookData(False).values())
        minLineLen = int(max(map(lambda d: len(d), dataToRemove)) * 1.5)

        for currentNum in range(0, maxLines):
            if currentNum < len(headLines):
                currentLine = headLines[currentNum]
                currentText = currentLine.text
                if (currentText == None or len(currentText) > minLineLen):
                    continue
                if any(currentText.lower().find(content.lower()) != -1 for content in dataToRemove):
                    currentLine.getparent().remove(currentLine)

    def output(self, path, zip):
        xml = self.getXmlContent()
        if xml != None:
            if zip:
                print('Writing file %s' % path)
                contentFile = ntpath.basename(path)
                newZip = ZipFile('%s.zip' % path, 'w')
                newZip.writestr(contentFile, etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
                newZip.close()
            else:
                print('Writing file %s' % path)
                newFile = open(path, 'wb')
                newFile.write(etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
                newFile.close()
