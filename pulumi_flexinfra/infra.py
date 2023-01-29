""" The Infra class handles calling the common methods on all providers
In most cases, this will be the main class the user interacts with.

They do not need to know how the specific providers work, they just need to
pass the correct generic objects to the Infra class.
"""

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
