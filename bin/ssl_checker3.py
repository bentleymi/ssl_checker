from __future__ import print_statement
import six
__doc__ = """
# Copyright 2016 Michael Camp Bentley aka JKat54 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
import subprocess, sys, os, re
from io import open

appBinDir = sys.path[0] 
splunkDir = os.path.join(appBinDir,'..','..','..','..')
splunkDir = os.path.normpath(splunkDir)
splunkBinDir = os.path.join(splunkDir,'bin')
splunkBinPath = os.path.join(splunkBinDir,"splunk")

sslConfigFiles = {}
sslConfigFiles['deploymentclient.conf'] = ['caCertFile']
sslConfigFiles['inputs.conf'] = ['serverCert','caCertFile','caPath','sslRootCAPath','rootCA','sslKeysfile']
sslConfigFiles['outputs.conf'] = ['clientCert','sslCertPath','sslRootCAPath']
sslConfigFiles['server.conf'] = ['serverCert','caCertFile','caPath','sslRootCAPath','rootCA','sslKeysfile']
sslConfigFiles['web.conf'] = ['serverCert','caCertPath']
uniqueSSLConfigKeys = ['caCertFile','caPath','clientCert','rootCA','serverCert','sslKeysfile','sslRootCAPath']

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            yield os.path.join(root,name)

foundConfigFiles = {}
for configFile in sslConfigFiles:
    for foundConfigFile in find(configFile,splunkDir):
        foundConfigFiles[foundConfigFile] = []

foundSSLPaths = {}
foundSSLPaths['sslPaths'] = {}
foundCAPaths = {}
foundCAPaths['caPaths'] = {}
for configFilePath in foundConfigFiles:
    sslKeyMatches = 0
    caPathMatches = 0
    for key in uniqueSSLConfigKeys:
        pattern = re.compile("^" + key + "\s+?\=\s+?(.*\.[Pp][Ee][Mm])")
        for i, line in enumerate(open(configFilePath)):
            for match in re.finditer(pattern,line):
                foundSSLPaths['sslPaths'][match.group(1)] = True
                sslKeyMatches = sslKeyMatches + 1
        pattern = re.compile("^caPath\s+?\=\s+?(.*)")
        for i, line in enumerate(open(configFilePath)):
            for match in re.finditer(pattern,line):
                foundCAPaths['caPaths'][match.group(1)] = True
                caPathMatches = caPathMatches + 1
    if sslKeyMatches >= 1:
        foundConfigFiles[configFilePath].append(foundSSLPaths)
    if caPathMatches >= 1:
        foundConfigFiles[configFilePath].append(foundCAPaths)

certsToCheckTemp = {}
certsToCheck = {}
for configFile in foundConfigFiles:
 for item in foundConfigFiles[configFile]:
  if 'sslPaths' in item:
   for sslPath in item['sslPaths']:
    sslPath = sslPath.replace("$SPLUNK_HOME",splunkDir)
    match = re.match("^[\/|\\\\]",sslPath)
    if match:
     certsToCheckTemp[sslPath] = True
    else:
     sslPath = os.path.join("CA_PATH_HERE", sslPath)
     certsToCheckTemp[sslPath] = True
  if 'caPaths' in item:
   for caPath in item['caPaths']:
    caPath = caPath.replace("$SPLUNK_HOME",splunkDir)
    for cert in certsToCheckTemp:
     if re.match("CA_PATH_HERE",cert):
      certsToCheck[cert.replace("CA_PATH_HERE",caPath)] = True
     else:
      certsToCheck[cert] = True

for sslPath in certsToCheck:
    if sslPath:
        p1 = subprocess.Popen([splunkBinPath,"cmd","openssl","x509","-enddate","-noout","-in",sslPath], stdout=subprocess.PIPE)
        dates = str(p1.communicate()[0])
        p1.stdout.close()
        message = 'cert="' + sslPath + '" ' + dates.replace('=','="').replace('\n','"|').replace('|',' ')
        message = message.replace("notAfter","expires")
        print(message)
