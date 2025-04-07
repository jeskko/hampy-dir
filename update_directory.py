#!/usr/bin/env python3

import pandas as pd
import yaml
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

with open('config.yaml') as file:
    conf=yaml.safe_load(file)

sheetUrl = conf["sheet_url"]
outpath = conf["output_path"]
gs_outpath = conf["gs_output_path"]
webroot = conf["webroot_url"]

sheetDF = pd.read_csv(sheetUrl)
phonelist=sheetDF.values.tolist()[3:]

numpages=int(len(phonelist)/32)

# cisco, max 32 numbers per page

r=Element('CiscoIPPhoneMenu')
c=SubElement(r,"Title")
c.text="HamPY puhelinluettelo"
c=SubElement(r,"Prompt")
c.text="Valitse sivu"

for i in range(numpages+1):
    c=SubElement(r,"MenuItem")
    cc=SubElement(c,"Name")
    cc.text=f"Sivu {i+1}"
    cc=SubElement(c,"URL")
    cc.text=f"{webroot}directory_79x0_{i+1}.xml"
    
sr=minidom.parseString(tostring(r))
t=sr.toprettyxml(indent="  ", encoding="ISO-8859-15")
f=open(f"{outpath}/directory_79x0.xml","wb")
f.write(t)
f.close()


for j in range(numpages+1):
    start=j*32
    end=j*32+31
    if (end>len(phonelist)):
        end=len(phonelist)
    r=Element('CiscoIPPhoneDirectory')
    c=SubElement(r,"Title")
    c.text=f"HamPY puhelinluettelo, {j+1}/{numpages+1}"

    for i in phonelist[start:end]:
        num=i[0]
        name=i[1]
        desc=i[2]
        if type(desc)==str:
            desc=f" ({desc})"
        else:
            desc=""
        c=SubElement(r,"DirectoryEntry")
        cc=SubElement(c,"Name")
        cc.text=f"{name}{desc}"
        cc=SubElement(c,"Telephone")
        cc.text=num

    sr=minidom.parseString(tostring(r))
    t=sr.toprettyxml(indent="  ", encoding="ISO-8859-15")
    f=open(f"{outpath}/directory_79x0_{j+1}.xml","wb")
    f.write(t)
    f.close()

# cisco 7965

r=Element('CiscoIPPhoneMenu')
c=SubElement(r,"Title")
c.text="HamPY puhelinluettelo"
c=SubElement(r,"Prompt")
c.text="Valitse numero"
for i in phonelist:
    num=i[0]
    name=i[1]
    desc=i[2]
    if type(desc)==str:
        desc=f" ({desc})"
    else:
        desc=""
    c=SubElement(r,"MenuItem")
    cc=SubElement(c,"Name")
    cc.text=f"{name}{desc}"
    cc=SubElement(c,"URL")
    cc.text=f"Dial:{num}"
sr=minidom.parseString(tostring(r))
t=sr.toprettyxml(indent="  ", encoding="UTF-8")
f=open(f"{outpath}/directory.xml","wb")
f.write(t)
f.close()
    
# grandstream

r=Element('AddressBook')
for i in phonelist:
  num=i[0]
  name=i[1]
  desc=i[2]
  if type(desc)==str:
      desc=f"{desc}"
  else:
      desc=""
  c=SubElement(r,"Contact")
  cc=SubElement(c,"LastName")
  cc.text=desc
  cc=SubElement(c,"FirstName")
  cc.text=name
  cc=SubElement(c,"Phone")
  ccc=SubElement(cc,"phonenumber")
  ccc.text=f"{num}"
  ccc=SubElement(cc,"accountindex")
  ccc.text="1"
  cc=SubElement(c,"Groups")
  ccc=SubElement(cc,"groupid")
  ccc.text="0"
  
r=minidom.parseString(tostring(r))
t=r.toprettyxml(indent="  ")
f=open(f"{gs_outpath}/phonebook.xml","w")
f.write(t)
f.close()
