import gzip
from pathlib import Path
from json import dumps, loads
from google.protobuf.json_format import MessageToDict, Parse
from schema_pb2 import Backup

Path('.output').mkdir(exist_ok=True)

def t2j(f, o):
    msg = Backup()
    msg.ParseFromString(gzip.open(f, 'rb').read())
    o.write_text(dumps(MessageToDict(msg), indent=2))

def j2t(f, o):
    d = loads(f.read_text(encoding='utf-8'))
    with gzip.open(o, 'wb') as w:
        w.write(Parse(dumps(d), Backup()).SerializeToString())

inp = Path('.input')
out = Path('.output')
tachs = list(inp.glob('*.tachibk'))
jsons = list(inp.glob('*.json'))

if tachs:
    [t2j(f, out / (f.stem + '.json')) for f in tachs]
elif jsons:
    [j2t(f, out / (f.stem + '.tachibk')) for f in jsons]
else:
    print('No .tachibk or .json files found in input/')