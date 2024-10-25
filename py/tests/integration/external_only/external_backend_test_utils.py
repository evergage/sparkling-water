#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import subprocess
from pysparkling.conf import H2OConf


def createH2OConf():
    conf = H2OConf()
    conf.setClusterSize(1)
    conf.useAutoClusterStart()
    conf.setExternalClusterMode()
    conf.setLogLevel("INFO")
    return conf


def listYarnApps():
    return str(subprocess.check_output("yarn application -list", shell=True))


def noYarnApps():
    exp = "Total number of applications (application-types: [], states: [SUBMITTED, ACCEPTED, RUNNING] and tags: []):0"
    return exp in listYarnApps()


def yarnLogs(appId):
    return str(subprocess.check_output("yarn logs -applicationId " + appId, shell=True))


def getYarnAppIdFromNotifyFile(path):
    with open(path, 'r') as f:
        return f.readlines()[1].replace("job", "application").strip()


def getIpPortFromNotifyFile(path):
    with open(path, 'r') as f:
        return f.readlines()[0].strip()
