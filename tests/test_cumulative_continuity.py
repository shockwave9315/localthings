"""Regression tests for cumulative counter capability/state continuity."""

from typing import cast

from homeassistant.components.sensor import RestoreSensor
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from custom_components.localthings.const import DOMAIN
from custom_components.localthings.coordinator import LocalThingsCoordinator
from custom_components.localthings.entity import _is_included
from custom_components.localthings.registry.adapter import _key
from custom_components.localthings.registry.capability import Capability
from custom_components.localthings.registry.discovery import BoundEntity
from custom_components.localthings.registry.entities import SensorDesc
from custom_components.localthings.sensor import LocalThingsRetainedSensor


class _FakeConfigEntry:
    options: dict = {}


class _FakeCoordinator:
    """Minimal coordinator surface needed by entity/sensor continuity tests."""

    def __init__(self, resources=None, *, hass=None):
        self.hass = hass
        self.device_key = "TEST-DEVICE"
        self.config_entry = _FakeConfigEntry()
        self.last_resources = resources or {}
        self.data: dict = {}

    @property
    def discovery_resources(self):
        return self.last_resources

    def discovery_canonical(self, subdevice):
        return self.last_resources

    def canonical_resources(self, subdevice):
        return self.last_resources

    def resource(self, href):
        return self.last_resources.get(href, {})


def _energy_bound() -> BoundEntity:
    desc = SensorDesc(
        key="energy_kwh",
        field="x.com.samsung.da.cumulativePower",
        device_class="energy",
        state_class="total_increasing",
        unit="kWh",
        exists_fn=lambda rep, resources: "x.com.samsung.da.cumulativePower" in rep,
    )
    capability = Capability(href="/energy/consumption/vs/0", entities=(desc,))
    return BoundEntity(href=capability.href, capability=capability, desc=desc)


async def test_registered_cumulative_sensor_survives_transient_field_loss(
    hass: HomeAssistant,
) -> None:
    """A known counter stays registered when its non-empty resource omits the total."""
    bound = _energy_bound()
    coordinator = _FakeCoordinator(
        {
            bound.href: {
                "x.com.samsung.da.instantaneousPower": "-500",
                "x.com.samsung.da.cumulativeUnit": "Wh",
                "x.com.samsung.da.cumulativeDate": "0",
            }
        },
        hass=hass,
    )
    unique_id = f"{DOMAIN}_{coordinator.device_key}_{_key(bound)}"
    er.async_get(hass).async_get_or_create(
        "sensor",
        DOMAIN,
        unique_id,
        suggested_object_id="test_energy",
    )

    assert _is_included(bound, cast(LocalThingsCoordinator, coordinator)) is True


async def test_unproven_cumulative_sensor_still_uses_capability_gate(
    hass: HomeAssistant,
) -> None:
    """A new device does not gain a phantom sensor from unrelated populated fields."""
    bound = _energy_bound()
    coordinator = _FakeCoordinator(
        {bound.href: {"x.com.samsung.da.instantaneousPower": "-500"}}, hass=hass
    )

    assert _is_included(bound, cast(LocalThingsCoordinator, coordinator)) is False


async def test_confirmed_empty_resource_does_not_resurrect_registered_counter(
    hass: HomeAssistant,
) -> None:
    """Preserve issue #127: a genuinely empty energy rep still means unsupported."""
    bound = _energy_bound()
    coordinator = _FakeCoordinator({bound.href: {}}, hass=hass)
    unique_id = f"{DOMAIN}_{coordinator.device_key}_{_key(bound)}"
    er.async_get(hass).async_get_or_create(
        "sensor",
        DOMAIN,
        unique_id,
        suggested_object_id="test_energy",
    )

    assert _is_included(bound, cast(LocalThingsCoordinator, coordinator)) is False


def test_cumulative_sensor_holds_last_value_until_new_total_arrives() -> None:
    """Missing flattened data holds the last total; a later real total wins immediately."""
    bound = _energy_bound()
    coordinator = _FakeCoordinator()
    sensor = LocalThingsRetainedSensor(cast(LocalThingsCoordinator, coordinator), bound)

    coordinator.data = {"energy_kwh": 92.4}
    assert sensor.native_value == 92.4

    coordinator.data = {}
    assert sensor.native_value == 92.4

    coordinator.data = {"energy_kwh": None}
    assert sensor.native_value == 92.4

    coordinator.data = {"energy_kwh": 92.7}
    assert sensor.native_value == 92.7


def test_cumulative_sensor_uses_home_assistant_restore_mixin() -> None:
    """Retained totals are persisted by HA so reloads can start from the last value."""
    assert issubclass(LocalThingsRetainedSensor, RestoreSensor)
