from Parser import parser

group = parser.add_group(__file__,__doc__,"Class")
group.add_argument('--raw-output',help='print tables without fancy separators (perhaps better for importing to excel)',action='store_true',default=False)

class Table:
    def __init__(self,header):
        # header = [SampleNames,Column1,Column2,...]
        self.header = header
        self.table = []
        self.nspaces = [ len(h) for h in header ]
        self.num_temp = '%.6g'
        parser.parse_args()
    def addRow(self,row):
        if len(row) != len(self.header):
            print 'Current header length %i' % len(self.header)
            print 'Input row has length  %i' % len(row)
            return
        for i,c in enumerate(row):
            v = c if type(c) == str else self.num_temp % c
            self.nspaces[i] = max( self.nspaces[i],len(v) )
        self.table.append(row)
        
    def __str__(self):
        str_table = []
        for row in self.table:
            str_row = []
            for v in row:
                if type(v) == str: str_row.append(v)
                else:              str_row.append( self.num_temp % v )
            str_table.append(str_row)
        def RowStr(row,sep,raw=False):
            rowstr = []
            for i,col in enumerate(row):
                if not raw:rowstr.append( col.center(self.nspaces[i]) )
                else: rowstr.append(col)
            return sep.join(rowstr)
        def RowSep(char): return char*( sum(self.nspaces)+3*len(self.nspaces) )
        lines = [ ]
        if parser.args.raw_output:
            rowdivide = ' '
            coldivide = '|'
        else:
            rowdivide = '-'
            coldivide = ' | '
            lines.append( RowSep('=') )
            
        rowsep = RowSep(rowdivide)
        lines.append(RowStr(self.header,coldivide,raw=parser.args.raw_output))
        if not parser.args.raw_output: lines.append( rowsep )
        for row in str_table:
            lines.append( RowStr(row,coldivide,raw=parser.args.raw_output) )
            if not parser.args.raw_output: lines.append( rowsep )
        return '\n'.join(lines)

class TableSet:
    tablelist = []
    nspaces = []
    def add(self,table): self.tablelist.append(table)
    def __str__(self):
        for table in self.tablelist:
            for i,nspace in enumerate(table.nspaces):
                if len(self.nspaces) <= i: self.nspaces.append(nspace)
                self.nspaces[i] = max( self.nspaces[i],nspace )
        for table in self.tablelist:
            table.onspace = [ nspace for nspace in table.nspaces ]
            for i,nspace in enumerate(table.nspaces):
                table.nspaces[i] = self.nspaces[i]
        tablestr = [ str(table) for table in self.tablelist ]
        return '\n'.join(tablestr)
                
