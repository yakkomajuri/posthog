from typing import Optional, Union
from uuid import UUID

from django.conf import settings

from posthog.models.organization import Organization


# We disable Plugins on Cloud, except for whitelisted organizations
# Disregarding this in TEST mode, so that we can be sure plugins actually work in EE if/when needed
def guard_cloud(organization_or_id: Optional[Union[Organization, UUID, str]]):
    organization_id: Optional[str] = (
        None
        if not organization_or_id
        else str(organization_or_id if isinstance(organization_or_id, (str, UUID)) else organization_or_id.id)
    )
    return settings.TEST or not getattr(settings, "MULTI_TENANCY", False)


def can_install_plugins_via_api(organization_or_id: Union[Organization, str, UUID]) -> bool:
    if not settings.PLUGINS_INSTALL_VIA_API:
        return False
    if settings.MULTI_TENANCY:
        return True
    organization: Organization = (
        organization_or_id
        if isinstance(organization_or_id, Organization)
        else Organization.objects.get(id=organization_or_id)
    )
    return organization.plugins_access_level >= Organization.PluginsAccessLevel.INSTALLATION


def can_configure_plugins_via_api(organization_or_id: Union[Organization, str, UUID]) -> bool:
    if not settings.PLUGINS_CONFIGURE_VIA_API:
        return False
    if settings.MULTI_TENANCY:
        return True
    organization: Organization = (
        organization_or_id
        if isinstance(organization_or_id, Organization)
        else Organization.objects.get(id=organization_or_id)
    )
    return organization.plugins_access_level >= Organization.PluginsAccessLevel.CONFIGURATION
