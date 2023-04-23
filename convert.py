import xml.etree.ElementTree as ET
import pandas as pd

FILENAME = "DLTINS_20210118_01of01"
csv_columns = [
    "FinInstrmGnlAttrbts.Id",
    "FinInstrmGnlAttrbts.FullNm",
    "FinInstrmGnlAttrbts.ClssfctnTp",
    "FinInstrmGnlAttrbts.CmmdtyDerivInd",
    "FinInstrmGnlAttrbts.NtnlCcy",
    "Issr",
    "{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}Id"
]

df = pd.DataFrame(columns=csv_columns)

for _, element in ET.iterparse(f"{FILENAME}.xml", events=("start",)):
    if "TermntdRcrd" in element.tag:
        data = {}
        for child in element:
            if "FinInstrmGnlAttrbts" in child.tag:
                for subchild in child:
                    data[csv_columns[csv_columns.index(subchild.tag)]] = subchild.text
            elif "Issr" in child.tag:
                data[csv_columns[5]] = child.text
        df = df.append(data, ignore_index=True)

df.dropna(inplace=True)
df.to_csv(f"{FILENAME}.csv", index=False)
