#!/usr/bin/env python3
"""Download NDW public charging locations and create small geographic JSON tiles."""
import gzip,json,math,pathlib,urllib.request,datetime,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
URL='https://opendata.ndw.nu/charging_point_locations.geojson.gz'
req=urllib.request.Request(URL,headers={'User-Agent':'ChargeUp-public-data-sync/1.0'})
with urllib.request.urlopen(req,timeout=120) as response:
    data=gzip.decompress(response.read())
obj=json.loads(data)
if not isinstance(obj.get('features'),list) or len(obj['features'])<100:
    raise ValueError('NDW response does not look like nationwide GeoJSON')
tiles={}
for i,f in enumerate(obj['features']):
    g=f.get('geometry') or {}; p=f.get('properties') or {}
    if g.get('type')!='Point':continue
    c=g.get('coordinates') or []
    if len(c)<2:continue
    try: lon,lat=float(c[0]),float(c[1])
    except (TypeError,ValueError):continue
    if not (3<=lon<=8 and 50<=lat<=54):continue
    access=str(p.get('access') or p.get('access_type') or '').lower()
    if access in ('private','no','restricted_private'):continue
    name=p.get('name') or p.get('location_name') or p.get('operator_name') or 'Openbaar laadpunt'
    operator=p.get('operator_name') or p.get('operator') or ''
    address=p.get('address') if isinstance(p.get('address'),dict) else {}
    street=address.get('street') or p.get('street') or ''
    house=address.get('house_number') or p.get('house_number') or ''
    city=address.get('city') or p.get('city') or ''
    power=p.get('max_electric_power') or p.get('max_power') or p.get('power') or ''
    key=f'{math.floor(lon*10)}_{math.floor(lat*10)}'
    item={'id':str(p.get('id') or p.get('location_id') or f.get('id') or f'{lon:.6f}:{lat:.6f}'), 'lat':lat,'lon':lon,'source':'DOT-NL','tags':{'name':str(name),'operator':str(operator),'addr:street':str(street),'addr:housenumber':str(house),'addr:city':str(city),'charging_station:output':str(power)}}
    tiles.setdefault(key,[]).append(item)
out=ROOT/'data';out.mkdir(exist_ok=True)
folder=out/'tiles'
if folder.exists():shutil.rmtree(folder)
folder.mkdir()
for key,items in tiles.items():
    (folder/(key+'.json')).write_text(json.dumps(items,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
manifest={'updated':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':URL,'total':sum(map(len,tiles.values())),'tiles':sorted(tiles)}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('NDW locations:',manifest['total'],'tiles:',len(tiles))
