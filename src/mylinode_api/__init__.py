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
        """Linode Client

        Args:
            TOKEN: Specify token from cloud manager.
        """
        self.token = TOKEN
        self.authHeader = {"Authorization": f"Bearer {self.token}"}
        
    # Linode methods:
    def getLinodes(self):
        """Get list of linodes if you have `read` permissions.

        Returns:
            Returns a list of your linodes.
        """
        linodesList = []
        linodesListRequest = requests.get("https://api.linode.com/v4/linode/instances", headers=self.authHeader).json()
        
        for i in linodesListRequest['data']:
            linodesList.append(i['id'])
        return linodesList
    
    def createLinode(self, region:str, type:str, image:str, root_pass:str, **kwargs):
        """Create a new linode server if you have `write` permissions.

        Args:
            region: Region of server
            type: Server plan
            image: The linux image of the server.
            root_pass: The root password of the server.

        Raises:
            Will raise errors if region, type or/and image is not found.

        Returns:
            Returns the json response.
        """
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
        return handleRequestError(response)
    
    def deleteLinode(self, linodeID:int):
        """Delete Linode if you have `read_write` permissions.

        Args:
            linodeID: The ID of the linode that will be removed.

        Returns:
            true (boolean) if success.
        """
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}", headers=self.authHeader)
        return handleRequestError(response)
    
    def findLinode(self, linodeID:int):
        """View Linode if you have `read` permissions.

        Args:
            linodeID: The LinodeID.

        Returns:
            Returns a dictionary of the found Linode.
        """
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}", headers=self.authHeader)
        return handleRequestError(response)
        
    def updateLinode(self, linodeID:int, **kwargs):
        """Update Linode if you have `read_write` permissions.

        Args:
            linodeID: The linode ID that will be updated.
            kwargs: Other parameters (can be found in 
            https://www.linode.com/docs/api/linode-instances/#linode-update
            )

        Returns:
            Returns the response of the linode with the updated changes.
        """
        data = kwargs
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{linodeID}", json=data, headers=self.authHeader)
        return handleRequestError(response)
        
    def bootLinode(self, linodeID:int):
        """Turn on the linode if you have `read_write` permissions.

        Args:
            linodeID: The linodeID that will be booted.

        Returns:
            true (boolean) if success.
        """
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/boot", headers=self.authHeader)
        return handleRequestError(response)
        
    def rebootLinode(self, linodeID:int):
        """Restarts the linode if you have `read_write` permissions

        Args:
            linodeID: The linodeID that will be rebooted.

        Returns:
            true (boolean) if success.
        """
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/reboot", headers=self.authHeader)
        return handleRequestError(response)
        
    def resetPassLinode(self, linodeID:int, password:str):
        """Reset password of Linode if you have `read_write` permissions

        Args:
            linodeID: The linodeID that will be restarted
            password: The new password of the linode.

        Returns:
            true (boolean) if success.
        """
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/password", headers=self.authHeader, json={"root_pass": password})
        return handleRequestError(response)
        
    def rebuildLinode(self, linodeID:int, image:str, root_pass:str, **kwargs):
        """Rebuilds a Linode you have the `read_write` permission to modify.

        Args:
            linodeID: The linodeID
            image: The new image of the server.
            root_pass: The new password of the server.

        Returns:
            Returns a json response of the new linode.
        """
        data = {"image": image, "root_pass": root_pass}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/rebuild", headers=self.authHeader, json=data)
        return handleRequestError(response)
        
    def shutDownLinode(self, linodeID:int):
        """Stop the Linode server if you have `write` permission.

        Args:
            linodeID (int): _description_

        Returns:
            true (boolean) if success.
        """
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/shutdown")
        return handleRequestError(response)
        
    def statisticsLinode(self, linodeID:int):
        """Gets the statistics of the linode if you have `read` permissions.

        Args:
            linodeID: The linodeID.

        Returns:
            Returns a json with the statistics.
        """
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/stats", headers=self.authHeader)
        return handleRequestError(response)
        
    def cloneLinode(self, linodeID:int, **kwargs):
        """Clones the linode into a new linode if you have `read_write` permissions.

        Args:
            linodeID: The linodeID that will be cloned.

        Returns:
            Returns a json of the new Linode.
        """
        data = kwargs
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/clone", headers=self.authHeader, json=data)
        return handleRequestError(response)
        
    def volumeListLinode(self, linodeID:int):
        """List of volumes in a linode if you have `read` permissions.

        Args:
            linodeID (int): _description_

        Returns:
            _type_: _description_
        """
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/volumes", headers=self.authHeader)
        return handleRequestError(response)
        
    def upgradeLinode(self, linodeID:int, **kwargs):
        """Upgrade a linode if you have `read_write` permissions

        Args:
            linodeID (int): _description_

        Returns:
            _type_: _description_
        """
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{linodeID}/mutate", headers=self.authHeader)
        return handleRequestError(response)
        
    # Backup methods:
        
    def getBackups(self, linodeID:int):
        """Get the backups of the linode if you have `read` permissions

        Args:
            linodeID: The linodeID.

        Returns:
            Returns the response json.
        """
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups", headers=self.authHeader)
        return handleRequestError(response)
        
    def cancelBackups(self, linodeID:int):
        """Cancel backups for a linode if you have `read_write` permissions.

        Args:
            linodeID: The ID of the linode that the backups will be canceled in.

        Returns:
            true (boolean) if success.
        """
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/cancel", headers=self.authHeader)
        return handleRequestError(response)
        
    def enableBackups(self, linodeID:int):
        """Enable backups for a linode if you have `read_write` permissions.

        Args:
            linodeID (int): _description_

        Returns:
            true (boolean) if success.
        """
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/enable", headers=self.authHeader)
        return handleRequestError(response)
        
    def findBackup(self, linodeID:int, backupID:int):
        """Find the backup of a linode

        Args:
            linodeID: The ID of the linode the backup is in.
            backupID: The ID of the backup (can be found with the `getBackups` method.)

        Returns:
            The response json.
        """
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/{str(backupID)}", headers=self.authHeader)
        return handleRequestError(response)
        
    def restoreBackup(self, linodeID:int, backupID:int):
        """Restore the backup of a linode

        Args:
            linodeID: The ID of the linode the backup is in.
            backupID: THe ID of the backup.

        Returns:
            true (boolean) if success.
        """
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups/{str(backupID)}/restore")
        return handleRequestError(response)
        
    # Snapshot methods:
    
    #TODO: Add snapshot methods.
        
    # Configuration methods:
        
    def getConfigs(self, linodeID:int):
        """Get configurations of a linode.

        Args:
            linodeID: The ID of the linode.

        Returns:
            Returns response json.
        """
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs", headers=self.authHeader)
        return handleRequestError(response)
        
    def createConfig(self, linodeID:int, devices:dict, label:str, **kwargs):
        """Create a configuration for a linode.

        Args:
            linodeID: The ID of the linode
            devices (dict): A dictionary of device disks.
            label: The label of the configuration.

        Returns:
            Response json.
        """
        data = {"devices": devices, "label": label}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs", headers=self.authHeader, json=data)
        return handleRequestError(response)
        
    def deleteConfig(self, linodeID:int, configID:int):
        """Delete the configuration of a linode.

        Args:
            linodeID: The ID of the linode
            configID: The ID of the configuration.

        Returns:
            true (boolean) if success.
        """
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs/{str(configID)}")
        return handleRequestError(response)
        
    def findConfig(self, linodeID:int, configID:int):
        """Find the configuration

        Args:
            linodeID: The ID of the linode that the configuration is in.
            configID: The ID of the configuration (can be found in `getConfigs` method)

        Returns:
            Returns response json.
        """
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs/{str(configID)}", headers=self.authHeader)
        return handleRequestError(response)
        
    def updateConfig(self, linodeID:int, configID:int, **kwargs):
        """Update configuration

        Args:
            linodeID: The ID of the linode that the configuration is in.
            configID: The ID of the configuration (can be found in `getConfigs` method)

        Returns:
            Returns response json.
        """
        data = kwargs
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/configs/{str(configID)}", headers=self.authHeader, json=data)
        return handleRequestError(response)
        
    # Disk methods:
    
    def getDisks(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks", headers=self.authHeader)
        return handleRequestError(response)
        
    def createDisk(self, linodeID:int, size:int, **kwargs):
        data = {"size": size}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks", self.authHeader, json=data)
        return handleRequestError(response)
        
    def deleteDisk(self, linodeID:int, diskID:int):
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}", headers=self.authHeader)
        return handleRequestError(response)
        
    def findDisk(self, linodeID:int, diskID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}", headers=self.authHeader)
        return handleRequestError(response)
    
    def updateDisk(self, linodeID:int, diskID:int, **kwargs):
        data = kwargs
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}", headers=self.authHeader, json=data)
        return handleRequestError(response)
        
    def cloneDisk(self, linodeID:int, diskID:int):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}/clone", headers=self.authHeader)
        return handleRequestError(response)
        
    def resetPassDisk(self, linodeID:int, diskID:int, password:str):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}/password", headers=self.authHeader, json={"password": str(password)})
        return handleRequestError(response)
        
    def resizeDisk(self, linodeID:int, diskID:int, size:int):
        if not size>=1:
            raise ValueError("Size has to be bigger or equals to one.")
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/disks/{str(diskID)}/resize", headers=self.authHeader, json={"size": size})
        return handleRequestError(response)
        
    # IP Methods:
    
    def allocateIPv4(self, linodeID:int, public:bool, iptype="ipv4"):
        data = {"public": public, "type": iptype}
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/ips", headers=self.authHeader, json=data)
        return handleRequestError(response)
        
    def deleteIPv4(self, linodeID:int, address:str):
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{str(linodeClient())}/ips/{str(address)}")
        return handleRequestError(response)
        
    def findIP(self, linodeID:int, address:str):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/ips/{str(address)}", headers=self.authHeader)
        return handleRequestError(response)
        
    def RDNSUpdateIP(self, linodeID:int, address:str, rdns:str):
        response = requests.put(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/ips/{address}", headers=self.authHeader, json={"rdns": rdns})
        return handleRequestError(response)
        
    # Kernel Methods:
    
    def getKernels(self):
        response = requests.get("https://api.linode.com/v4/linode/kernels", headers=self.authHeader)
        return handleRequestError(response)
    
    def findkernel(self, kernelID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/kernels/{str(kernelID)}", headers=self.authHeader)
        return handleRequestError(response)
    
    # Image Methods:
    
    def createImage(self, diskID:int, **kwargs):
        data = {"disk_id": diskID}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post("https://api.linode.com/v4/images", headers=self.authHeader, json=data)
        return handleRequestError(response)
    
    def uploadImage(self, label:str, region:str, **kwargs):
        data = {"label": label, "region": region}
        for i, (k, v) in enumerate(kwargs.items()):
            if v:
                data[k] = v
        response = requests.post("https://api.linode.com/v4/images/upload", headers=self.authHeader, json=data)
        return handleRequestError(response)
    
    def deleteImage(self, imageID:str):
        response = requests.delete(f"https://api.linode.com/v4/images/{str(imageID)}", headers=self.authHeader)
        return handleRequestError(response)
    
    def findImage(self, imageID:str):
        response = requests.get(f"https://api.linode.com/v4/images/{str(imageID)}", headers=self.authHeader)
        return handleRequestError(response)
    
    # Ohter Methods:
        
    def createSnapshot(self, linodeID:int, label:str):
        response = requests.post(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/backups", headers=self.authHeader, json={"label": label})
        return handleRequestError(response)
    
    def getFirewalls(self, linodeID:int):
        response = requests.get(f"https://api.linode.com/v4/linode/instances/{str(linodeID)}/firewalls", headers=self.authHeader)
        return handleRequestError(response)
    
    #TODO: Add more methods