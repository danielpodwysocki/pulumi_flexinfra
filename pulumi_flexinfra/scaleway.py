""" A module to define a provider for Scaleway
"""
import logging

import pulumiverse_scaleway as scaleway

from pulumi_flexinfra.provider import Provider


logger = logging.getLogger(__name__)


class ScalewayProvider(Provider):
    """A class to define a provider for Scaleway
    :param provider_config: a dictionary containing the configuration for Scaleway
    It can contain the following keys:
    :type provider_config: dict
    """

    def set_images(self):
        # curl -s 'https://api-marketplace.scaleway.com/images?page=1&per_page=100' | sed 's/par1/fr-par-1/g; s/ams1/nl-ams-1/g' | jq '.images | map({"key": .label | gsub("_";"-"), "value": .versions[0].local_images}) | from_entries' | grep -i rock
        self.images = {
            "ubuntu22": "ubuntu_jammy",
            "debian11": "debian_bullseye",
            "rocky9": "rockylinux_9",
            "centos7": "centos_7.9",
        }

    def set_sizes(self):
        self.sizes = {
            "small": "DEV1-S",
            "medium": "DEV1-M",
            "large": "DEV1-L",
            "xlarge": "DEV1-XL",
        }

    def provision_server(self, server):
        if self.server_object_is_valid(server):
            ip = scaleway.InstanceIp(f"public_ip_{server.name}")
            server_instance = scaleway.InstanceServer(
                server.name,
                image=self.images[server.image],
                type=self.sizes[server.size],
                ip_id=ip.id,
            )

            self.servers.append(server)
        else:
            raise Exception("Invalid server object")


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
        pass


class Server:
    """A class representing a server.
    It can be passed to a provider to provision it. The configuration doesn't
    need to be changed for each provider - it is universal.
    :param name: the name of the server
    :type name: str
    :param size: the size of the server. Should be one of the items in the sizes
    list
    :type size: str
    :param image: the image to use for the server. Should be one of the items in
    the images list
    :type image: str
    :param ip_address: the IP address to assign to the server
    :type ip_address: str
    """

    def __init__(
        self, name: str, size: str, image: str, ip_address: str = None
    ) -> None:
        self.name = name
        self.size = size
        self.image = image
        self.ip_address = ip_address
        pass

    def deploy(self):
        """Apply Ansible to the host"""
        pass
