""" A module to define a provider for Hetzner Cloud
"""

import logging

import pulumi_hcloud as hcloud

from pulumi_flexinfra.provider import Provider

logger = logging.getLogger(__name__)


class HCloudProvider(Provider):
    """A class to define a provider for Hetzner Cloud
    :param provider_config: a dictionary containing the configuration for HCloud
    It can contain the following keys:
    - network_config: a dictionary containing the configuration for the
    private network. It can contain the following keys:
        - private_ip_range (str): the main IP range for the network
        - subnets: a list of dictionaries containing the configuration for the
        subnets. Each dictionary can contain the following keys:
            - subnet_ip_range (str): the IP range for the subnet
            - name (str): the name of the subnet
    - location (str) - the location to use for the servers, for example "fsn1"
    :type provider_config: dict
    """

    def set_images(self):
        self.images = {
            "ubuntu22": "ubuntu-20.04",
            "debian11": "debian-11",
            "rocky8": "rocky-8",
            "rocky9": "rocky-9",
            "centos7": "centos-7",
        }

    def set_sizes(self):
        self.sizes = {
            "small": "cx11",
            "medium": "cx21",
            "large": "cx31",
            "xlarge": "cx41",
        }

    def provision_private_network(self):
        logger.info("Provisioning private network")
        return hcloud.Network(
            "network",
            ip_range=self.provider_config["network_config"]["private_ip_range"],
        )

    def provision_private_subnets(self):
        ret = []
        for subnet in self.provider_config["network_config"]["subnets"]:
            ret.append(
                hcloud.NetworkSubnet(
                    subnet["name"],
                    network_id=self.network.id,
                    ip_range=subnet["subnet_ip_range"],
                    network_zone="eu-central",
                    type="cloud",
                )
            )
        return ret

    def provision_server(self, server):
        """Provision a server
        :param server: a Server object
        :type server: Server
        """
        if self.server_object_is_valid(server):
            server_instance = hcloud.Server(
                server.name,
                server_type=self.sizes[server.size],
                image=self.images[server.image],
                ssh_keys=self.ssh_keys,
                networks=[
                    hcloud.ServerNetworkArgs(
                        network_id=self.network.id, ip=server.ip_address
                    )
                ],
                location=self.provider_config["location"],
                labels=server.tags,
            )
            self.servers.append(server_instance)
        else:
            raise Exception("Invalid server object")
