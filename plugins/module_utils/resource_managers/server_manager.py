# Copyright: (c) 2024, Cherry Servers UAB <info@cherryservers.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Manage Cherry Servers server resources."""
import time
from typing import Optional, List

from .. import normalizers
from .resource_manager import ResourceManager, Request, Method


class ServerManager(ResourceManager):
    """Manage Cherry Servers server resources."""

    DEFAULT_TIMEOUT = 120

    @property
    def name(self) -> str:
        """Cherry Servers server resource name."""
        return "server"

    def _normalize(self, resource: dict) -> dict:
        return normalizers.normalize_server(resource)

    def get_by_id(self, server_id: int) -> Optional[dict]:
        """Get a single Cherry Servers server resource, by its ID."""
        return self.perform_request(
            Request(
                method=Method.GET,
                url=f"servers/{server_id}",
                valid_status_codes=(200, 404),
                timeout=self.DEFAULT_TIMEOUT,
                params=None,
            )
        )

    def get_by_project_id(self, project_id: int) -> List[dict]:
        """Get a list of Cherry Servers server resources, by project ID."""
        return self.perform_request(
            Request(
                method=Method.GET,
                url=f"projects/{project_id}/servers",
                valid_status_codes=(200,),
                timeout=self.DEFAULT_TIMEOUT,
                params=None,
            )
        )

    def create_server(self, project_id: int, params: dict, timeout: int = DEFAULT_TIMEOUT) -> dict:
        """Create a Cherry Servers server resource."""
        return self.perform_request(
            Request(
                method=Method.POST,
                url=f"projects/{project_id}/servers",
                valid_status_codes=(201,),
                timeout=timeout,
                params=params,
            )
        )

    def update_server(self, server_id: int, params: dict, timeout: int = DEFAULT_TIMEOUT) -> dict:
        """Update a Cherry Servers server resource."""
        return self.perform_request(
            Request(
                method=Method.PUT,
                url=f"servers/{server_id}",
                valid_status_codes=(201,),
                timeout=timeout,
                params=params,
            )
        )

    def reinstall_server(
        self, server_id: int, params: dict, timeout: int = DEFAULT_TIMEOUT
    ) -> dict:
        """Reinstall a Cherry Servers server resource."""
        return self.perform_request(
            Request(
                method=Method.POST,
                url=f"servers/{server_id}/actions",
                valid_status_codes=(201, 202),
                timeout=timeout,
                params=params,
            )
        )

    def delete_server(self, server_id: int, timeout: int = DEFAULT_TIMEOUT):
        """Delete a Cherry Servers server resource."""
        self.perform_request(
            Request(
                method=Method.DELETE,
                url=f"servers/{server_id}",
                timeout=timeout,
                params=None,
                valid_status_codes=(204,),
            )
        )

    def wait_for_active(self, server: dict, timeout: int = 1800) -> dict:
        """Wait for Cherry Servers server resource to become active."""
        time_passed = 0

        while server["status"] != "deployed":
            time.sleep(10)
            time_passed += 10

            server = self.get_by_id(server["id"])

            if time_passed >= timeout:
                self.module.fail_json(
                    msg=f"timed out waiting for {self.name} to become active"
                )

        return server
