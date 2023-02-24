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
import pulumi_hcloud as hcloud
import pulumiverse_scaleway as scaleway
import logging

logger = logging.getLogger(__name__)


class Infra:
    """A class representing all infrastracture
    for a given environment.
    :param providers: A dict of providers to use, each implementing the Provider interface
    The keys should be the provider name, and the values should be Provider objects
    :type providers: list
    """

    def __init__(self, providers) -> None:
        self.providers = providers

    def provision_server(self, server, provider_name):
        """Provision a server on a given provider
        :param server: a Server object
        :type server: Server
        :param provider_name: the name of the provider to use
        :type provider_name: str
        """
        self.providers[provider_name].provision_server(server)

    def deploy(self):
        """Apply Ansible to all servers"""
        raise NotImplementedError("Not implemented yet")


class SecurityGroup:
    """A uniform way to define security groups across providers"""

    def __init__(self, name, rules):
        self.name = name
        self.rules = rules


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
        # if all(k in network_config for k in ("private_ip_range", "subnets")) and type(
        #    network_config.get("subnets", None) == list )
        # ):
        #    return True
        # return False

    def server_object_is_valid(self, server):
        """Check if the server object is valid
        :param server: a Server object
        :type server: Server
        :todo: check if the IP address is valid
        """
        if server.image in self.images.keys() and server.size in self.sizes.keys():
            return True
        return False


class Server:
    """A class representing a server.
    It can be passed to a provider to provision it. The configuration doesn't
    need to be changed for each provider - it is universal.

    :param name: the name of the server
    :param size: the size of the server. Should be one of the items in the sizes
    list
    :param image: the image to use for the server. Should be one of the items in
    the images list
    :param ip_address: the IP address to assign to the server
    :param tags: a dict of KV pairs to assign to the server
    """

    def __init__(
        self,
        name: str,
        size: str,
        image: str,
        ip_address: str = None,
        tags: dict = {},
    ) -> None:
        self.name = name
        self.size = size
        self.image = image
        self.ip_address = ip_address
        self.tags = tags
        pass

    def deploy(self):
        """Apply Ansible to the host"""
        pass
