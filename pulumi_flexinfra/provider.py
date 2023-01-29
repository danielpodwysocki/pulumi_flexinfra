""" Those classes provide a set of abstractions to create and manage
infrastracture across cloud providers.

The idea is to allow the user to not have to worry about the underlying
provider and quickly migrate to a different one if needed.

For a provider to be functional, they must support:
- VPS (Server class)
- Private networks and subnets
- Security groups/Firewall rules
"""

from abc import ABC
import logging

logger = logging.getLogger(__name__)


class Provider(ABC):
    """A class to define a cloud-agnostic interface for all my infra
    It allows the Infra class to have a reliable way of creating and managing
    infrastracture across cloud providers.
    :param provider_config: a dictionary containing the configuration for the
    specific provider
    It can contain the following keys:
    - network_config: a dictionary containing the configuration for the
    private network. It can contain the following keys:
        - private_ip_range (str): the main IP range for the network
        - subnets: a list of dictionaries containing the configuration for the
        subnets. Each dictionary can contain the following keys:
            - subnet_ip_range (str): the IP range for the subnet
            - name (str): the name of the subnet
    """

    def __init__(self, ssh_keys=None, provider_config=None) -> None:
        logger.info("Initializing provider, config: %s", provider_config)
        self.ssh_keys = ssh_keys
        self.provider_config = provider_config
        self.set_sizes()
        self.set_images()
        # if self.network_config_is_valid(self.provider_config["network_config"]):
        self.network = self.provision_private_network()
        self.subnets = self.provision_private_subnets()
        self.servers = []

    # @abstractmethod
    def set_sizes(self):
        """Set the sizes for the different types of servers
        Each provider class is expected to define the values for those
        keys on its own.
        """
        self.sizes = {
            "small": "instance_type_small",
            "medium": "instance_type_medium",
            "large": "instance_type_large",
            "xlarge": "instance_type_xlarge",
        }

    def set_images(self):
        """Set the images for different distros
        Each provider class is expected to define the values for those
        keys on its own.
        """
        self.images = {
            "ubuntu20": "ubuntu_20_04",
            "debian11": "debian_11",
            "rocky9": "rocky_9",
            "rocky8": "rocky_8",
        }

    def provision_private_network(self):
        pass

    def provision_private_subnets(self):
        pass

    def provision_server(self, size, image):
        """Provision a server
        :param size: the size of the server. Should be one of the keys in the
        sizes dictionary
        :type size: str
        :param image: the image to use for the server

        """
        pass

    def provision_security_group(self, security_group):
        """Provision a security group using the provider's API
        :param security_group: a SecurityGroup object
        """
        pass

    def network_config_is_valid(self, network_config):
        """Check if the network configuration is valid
        This can differ from provider to provider. For example, Hetzner supports
        subnets within your network, while Scaleway does not.
        By default, we assume that subnets are supported.
        :param network_config: a dictionary containing the network configuration
        :type network_config: dict
        :todo: implement this
        """
        return True

    def server_object_is_valid(self, server):
        """Check if the server object is valid
        :param server: a Server object
        :type server: Server
        :todo: check if the IP address is valid
        """
        if server.image in self.images.keys() and server.size in self.sizes.keys():
            return True
        return False
