import json
from decimal import Decimal

#Arredonda valor decimal
def decimalDefault(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

#Função de exportação dos dados ded conexão para arquivo JSON
def exportJson( data, columns, file = 'connections.json' ):
    dataList = [dict(zip(columns, row)) for row in data]
    with open(file, 'w') as f:
        json.dump(dataList, f, default = decimalDefault, indent = 4)