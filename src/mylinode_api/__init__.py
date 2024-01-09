import requests
import sys

def getRegions():
    regions = []
    regionRequest = requests.get("https://api.linode.com/v4/regions").json()
    for i in regionRequest['data']:
        regions.append(i['id'])
    return regions

def getTypes():
    types = []
    typesRequest = requests.get("https://api.linode.com/v4/linode/types").json()
    for i in typesRequest['data']:
        types.append(i['id'])
    return types

def getImages(private=False, token=None):
    images = []
    if private and token:
        imagesRequest = requests.get("https://api.linode.com/v4/images", headers={"Authorization": f"Bearer {token}"}).json()
    elif not private:
        imagesRequest = requests.get("https://api.linode.com/v4/images").json()
    for i in imagesRequest['data']:
        images.append(i['id'])
    return images

def keyByValue(dictionary: dict, value: any):
    key_list=list(dictionary.keys())
    val_list=list(dictionary.values())
    ind=val_list.index(value)
    return key_list[ind]

def handleRequestError(response):
    if 'errors' in response.json():
            for i in response.json()['errors']:
                raise ValueError(str(i['reason']))
    else:
        if response.json() == {}:
            return True
        else:
            return response.json()

class linodeClient:
    def __init__(self, TOKEN) -> None:
        self.token = TOKEN
        self.authHeader = {"Authorization": f"Bearer {self.token}"}
        
    # Linode methods:
    def getLinodes(self):
        linodesList = []
        linodesListRequest = requests.get("https://api.linode.com/v4/linode/instances", headers=self.authHeader).json()
        
        for i in linodesListRequest['data']:
            linodesList.append(i['id'])
        return linodesList
    
    def createLinode(self, region:str, type:str, image:str, root_pass:str, **kwargs):
        if region not in getRegions():
            raise ValueError("Region not found or not available.")
        if type not in getTypes():
            raise ValueError("Type not found or not available.")
        if image not in getImages(True, self.token):
            raise ValueError("Image not found or not available.")
        data = {
            "image": image,
            "type": type,
            "region": region,
            "root_pass": root_pass
        }
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post("https://api.linode.com/v4/linode/instances", json=data, headers=self.authHeader)
        handleRequestError(response)
    
    def deleteLinode(self, linodeID:int):
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}", headers=self.authHeader)
        handleRequestError(response)
    
    def findLinode(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}", headers=self.authHeader)
        handleRequestError(response)
        
    def updateLinode(self, linodeID:int, **kwargs):
        data = kwargs
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{linodeID}", json=data, headers=self.authHeader)
        handleRequestError(response)
        
    def bootLinode(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/boot", headers=self.authHeader)
        handleRequestError(response)
        
    def rebootLinode(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/reboot", headers=self.authHeader)
        handleRequestError(response)
        
    def resetPassLinode(self, linodeID:int, password:str):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/password", headers=self.authHeader, json={"root_pass": password})
        handleRequestError(response)
        
    def rebuildLinode(self, linodeID:int, image:str, root_pass:str, **kwargs):
        data = {"image": image, "root_pass": root_pass}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/rebuild", headers=self.authHeader, json=data)
        handleRequestError(response)
        
    def shutDownLinode(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/shutdown")
        handleRequestError(response)
        
    def statisticsLinode(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/stats", headers=self.authHeader)
        handleRequestError(response)
        
    def cloneLinode(self, linodeID:int, **kwargs):
        data = kwargs
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/clone", headers=self.authHeader, json=data)
        handleRequestError(response)
        
    def volumeListLinode(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/volumes")
        handleRequestError(response)
        
    def upgradeLinode(self, linodeID:int, **kwargs):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{linodeID}/mutate")
        
    # Backup methods:
        
    def getBackups(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups", headers=self.authHeader)
        handleRequestError(response)
        
    def cancelBackups(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/cancel", headers=self.authHeader)
        handleRequestError(response)
        
    def enableBackups(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/enable", headers=self.authHeader)
        handleRequestError(response)
        
    def findBackup(self, linodeID:int, backupID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/{str(backupID)}", headers=self.authHeader)
        handleRequestError(response)
        
    def restoreBackup(self, linodeID:int, backupID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/{str(backupID)}/restore")
        handleRequestError(response)
        
    # Snapshot methods:
        
    def createSnapshot(self, linodeID:int, label:str):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups", headers=self.authHeader, json={"label": label})
        handleRequestError(response)
        
    # Configuration methods:
        
    def getConfigs(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs", headers=self.authHeader)
        handleRequestError(response)
        
    def createConfig(self, linodeID:int, devices:dict, label:str, **kwargs):
        data = {"devices": devices, "label": label}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs", headers=self.authHeader, json=data)
        handleRequestError(response)
        
    def deleteConfig(self, linodeID:int, configID:int):
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs/{str(configID)}")
        handleRequestError(response)
        
    def findConfig(self, linodeID:int, configID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs/{str(configID)}", headers=self.authHeader)
        handleRequestError(response)
        
    def updateConfig(self, linodeID:int, configID:int, **kwargs):
        data = kwargs
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs/{str(configID)}", headers=self.authHeader, json=data)
        handleRequestError(response)
        
    # Disk methods:
    
    def getDisks(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks", headers=self.authHeader)
        handleRequestError(response)
        
    def createDisk(self, linodeID:int, size:int, **kwargs):
        data = {"size": size}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks", self.authHeader, json=data)
        handleRequestError(response)
        
    def deleteDisk(self, linodeID:int, diskID:int):
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}", headers=self.authHeader)
        handleRequestError(response)
        
    def findDisk(self, linodeID:int, diskID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}", headers=self.authHeader)
        handleRequestError(response)
    
    def updateDisk(self, linodeID:int, diskID:int, **kwargs):
        data = kwargs
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}", headers=self.authHeader, json=data)
        handleRequestError(response)
        
    def cloneDisk(self, linodeID:int, diskID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}/clone", headers=self.authHeader)
        handleRequestError(response)
        
    def resetPassDisk(self, linodeID:int, diskID:int, password:str):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}/password", headers=self.authHeader, json={"password": str(password)})
        handleRequestError(response)
        
    def resizeDisk(self, linodeID:int, diskID:int, size:int):
        if not size>=1:
            raise ValueError("Size has to be bigger or equals to one.")
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}/resize", headers=self.authHeader, json={"size": size})
        handleRequestError(response)
        
    # IP Methods:
    
    def allocateIPv4(self, linodeID:int, public:bool, iptype="ipv4"):
        data = {"public": public, "type": iptype}
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/ips", headers=self.authHeader, json=data)
        handleRequestError(response)
        
    def deleteIPv4(self, linodeID:int, address:str):
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeClient())}/ips/{str(address)}")
        handleRequestError(response)
        
    def findIP(self, linodeID:int, address:str):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/ips/{str(address)}", headers=self.authHeader)
        handleRequestError(response)
        
    def RDNSUpdateIP(self, linodeID:int, address:str, rdns:str):
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/ips/{address}", headers=self.authHeader, json={"rdns": rdns})
        handleRequestError(response)