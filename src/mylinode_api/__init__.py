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
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
    
    def deleteLinode(self, linodeID:int):
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
    
    def findLinode(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def updateLinode(self, linodeID:int, **kwargs):
        data = kwargs
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{linodeID}", json=data, headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def bootLinode(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/boot", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return True
        
    def rebootLinode(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/reboot", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return True
        
    def resetPassLinode(self, linodeID:int, password:str):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/password", headers=self.authHeader, json={"root_pass": password})
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return True
        
    def rebuildLinode(self, linodeID:int, image:str, root_pass:str, **kwargs):
        data = {"image": image, "root_pass": root_pass}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/rebuild", headers=self.authHeader, json=data)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def shutDownLinode(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/shutdown")
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return True
        
    def statisticsLinode(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/stats", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def cloneLinode(self, linodeID:int, **kwargs):
        data = kwargs
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/clone", headers=self.authHeader, json=data)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    # Backup methods:
        
    def getBackups(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def cancelBackups(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/cancel", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return True
        
    def enableBackups(self, linodeID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/enable", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return True
        
    def findBackup(self, linodeID:int, backupID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/{str(backupID)}", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def restoreBackup(self, linodeID:int, backupID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/{str(backupID)}/restore")
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return True
        
    # Snapshot methods:
        
    def createSnapshot(self, linodeID:int, label:str):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups", headers=self.authHeader, json={"label": label})
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    # Configuration methods:
        
    def getConfigs(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def createConfig(self, linodeID:int, devices:dict, label:str, **kwargs):
        data = {"devices": devices, "label": label}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs", headers=self.authHeader, json=data)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def deleteConfig(self, linodeID:int, configID:int):
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs/{str(configID)}")
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return True
        
    def findConfig(self, linodeID:int, configID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs/{str(configID)}", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def updateConfig(self, linodeID:int, configID:int, **kwargs):
        data = kwargs
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs/{str(configID)}", headers=self.authHeader, json=data)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    # Disk methods:
    
    def getDisks(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks", headers=self.authHeader)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()
        
    def createDisk(self, linodeID:int, size:int, **kwargs):
        data = {"size": size}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks", self.authHeader, json=data)
        errors = []
        if 'errors' in response.json():
            for i in response.json()['errors']:
                errors.append(i['reason'])
            print('\n'.join(errors))
            sys.exit(1)
        else:
            return response.json()