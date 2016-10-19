import urllib.request
import csv
from html.parser import HTMLParser

class HTMLTableParser(HTMLParser):
    """ This class serves as a html table parser. It is able to parse multiple
    tables which you feed in. You can access the result per .tables field.
    """
    def __init__(
        self,
        decode_html_entities=False,
        data_separator=' ',
    ):

        HTMLParser.__init__(self)

        self._parse_html_entities = decode_html_entities
        self._data_separator = data_separator

        self._in_td = False
        self._in_th = False
        self._current_table = []
        self._current_row = []
        self._current_cell = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        """ We need to remember the opening point for the content of interest.
        The other tags (<table>, <tr>) are only handled at the closing point.
        """
        if tag == 'td':
            self._in_td = True
        if tag == 'th':
            self._in_th = True

    def handle_data(self, data):
        """ This is where we save content to a cell """
        if self._in_td or self._in_th:
            self._current_cell.append(data.strip())

    def handle_charref(self, name):
        """ Handle HTML encoded characters """

        if self._parse_html_entities:
            self.handle_data(self.unescape('&#{};'.format(name)))

    def handle_endtag(self, tag):
        """ Here we exit the tags. If the closing tag is </tr>, we know that we
        can save our currently parsed cells to the current table as a row and
        prepare for a new row. If the closing tag is </table>, we save the
        current table and prepare for a new one.
        """
        if tag == 'td':
            self._in_td = False
        elif tag == 'th':
            self._in_th = False

        if tag in ['td', 'th']:
            final_cell = self._data_separator.join(self._current_cell).strip()
            self._current_row.append(final_cell)
            self._current_cell = []
        elif tag == 'tr':
            self._current_table.append(self._current_row)
            self._current_row = []
        elif tag == 'table':
            self.tables.append(self._current_table)
            self._current_table = []

typesAndUrlValue = {"Accident & Health Insurance (Financial)" : 431 ,"Chemicals - Major Diversified (Basic Materials)" : 110, "Diagnostic Substances (Healthcare)" :516,
            "Drug Delivery (Healthcare)": 513,"Drug Manufacturers - Major (Healthcare)":510,"Drug Manufacturers - Other (Healthcare)":511,"Drug Related Products (Healthcare)":514
            ,"Drug Stores (Services)" : 733,"Drugs - Generic (Healthcare)":512, "Drugs Wholesale (Services)": 756
            ,"Health Care Plans (Healthcare)":522 , "Hospitals (Healthcare)":524, "Long-Term Care Facilities (Healthcare)" : 523
            ,"Medical Appliances & Equipment (Healthcare)": 521,"Medical Equipment Wholesale (Services)":754, "Medical Instruments & Supplies (Healthcare)" : 520
            , "Medical Laboratories & Research (Healthcare)":525, "Medical Practitioners (Healthcare)":527, "Specialized Health Services (Healthcare)":528
            , "Specialty Chemicals (Basic Materials)":113, "Synthetics (Basic Materials)":111}


allTypesData = {key: [] for key in typesAndUrlValue.keys()} # dict.fromkeys(typesAndUrlValue.keys())


def get_html_table(target):
    req = urllib.request.Request(url=target)
    f = urllib.request.urlopen(req)
    xhtml = f.read().decode('utf-8')
    p = HTMLTableParser()
    p.tables = []
    p.feed(xhtml)
    return p


for field in typesAndUrlValue.keys():
    value = typesAndUrlValue[field]
    target = 'https://screener.finance.yahoo.com/b?sc=' + str(value) + \
             '&im=&prmin=&prmax=&mcmin=&mcmax=&dvymin=&dvymax=&betamin=&betamax=&remin=&remax=&pmmin=&pmmax=&pemin=&pemax=&pbmin=&pbmax=&psmin=&psmax=&pegmin=&pegmax=&gr=&grfy=&ar=&vw=1&db=stocks'
    p = get_html_table(target)
    numberOfStocks = p.tables[0][0][0].split(' ')[7].split(')')[0]
    count = 0
    b = 1
    while b <= int(numberOfStocks):
        newTarget = target+"&b="+str(b)
        p = get_html_table(newTarget)
        tmp = [x for i,x in enumerate(p.tables[1]) if i!=0]
        allTypesData[field] += tmp
        count += len(tmp)
        b += 20

    print(str(count)+" items where added to field= "+ field+" expect= "+str(numberOfStocks)+" currently have= "+str(len(allTypesData[field])))
    with open('{}.csv'.format(field), 'w') as csv_file:
        writer = csv.writer(csv_file)
        for stock in allTypesData[field]:
            writer.writerow(stock)

# for field in typesAndUrlValue.keys():
#     print(allTypesData[field])
#     print()


# target = 'https://screener.finance.yahoo.com/b?sc=528&im=&prmin=&prmax=&mcmin=&mcmax=&dvymin=&dvymax=&betamin=&betamax=&remin=&remax=&pmmin=&pmmax=&pemin=&pemax=&pbmin=&pbmax=&psmin=&psmax=&pegmin=&pegmax=&gr=&grfy=&ar=&vw=1&db=stocks'
#
# # get website content
# req = urllib.request.Request(url=target)
# f = urllib.request.urlopen(req)
# xhtml = f.read().decode('utf-8')
#
# # instantiate the parser and feed it
# p = HTMLTableParser()
# p.feed(xhtml)
# print(p.tables[1][1:-1])
