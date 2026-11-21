import { describe, it, expect, beforeEach } from 'vitest';
import '../src/appliance-card';
import { ApplianceCard } from '../src/appliance-card';

describe('Breville oven visual fixtures', () => {
  let element: ApplianceCard;
  beforeEach(() => {
    element = document.createElement('appliance-card') as ApplianceCard;
    document.body.appendChild(element);
  });

  const renderFixture = async (fixture: Record<string, any>) => {
    element.setConfig({
      type: 'custom:appliance-card', appliance_type: 'oven',
      breville_status_entity: 'sensor.breville_oven_status',
      temperature_entity: 'sensor.breville_oven_temperature',
      target_temperature_entity: 'number.breville_oven_target_temperature',
      mode_entity: 'sensor.breville_oven_active_mode',
      time_entity: 'sensor.breville_oven_time_remaining',
      door_entity: 'binary_sensor.breville_oven_door',
    });
    element.hass = { states: Object.fromEntries(Object.entries(fixture).map(([key, state]) => [
      key.startsWith('sensor.') || key.startsWith('number.') || key.startsWith('binary_sensor.') ? key : `sensor.breville_oven_${key}`,
      typeof state === 'string' ? { state, attributes: {} } : state,
    ])) } as any;
    await element.updateComplete;
    return element.shadowRoot!;
  };

  it('renders sanitized states across idle, ready, cooking, keep warm, done, and unavailable', async () => {
    for (const [raw, label] of [['idle', 'Idle'], ['ready', 'Ready for food'], ['cooking', 'Cooking'], ['keeping_warm', 'Keeping warm'], ['done', 'Done'], ['unavailable', 'Unavailable']]) {
      const root = await renderFixture({ status: raw });
      expect(root.querySelector('.breville-status')?.textContent).toContain(label);
    }
  });

  it('omits retained temperatures, door state, and countdowns for stale statuses', async () => {
    for (const status of ['offline', 'missing', 'unknown', 'updating', 'waiting_for_button']) {
      const root = await renderFixture({
        status,
        temperature: { state: '212', attributes: { unit_of_measurement: '°F' } },
        target_temperature: { state: '400', attributes: { unit_of_measurement: '°F' } },
        door: 'on',
        time_remaining: '12',
      });
      expect(root.querySelector('.breville-current-temp')).toBeNull();
      expect(root.querySelector('.breville-target-temp')).toBeNull();
      expect(root.querySelector('.breville-door-warning')).toBeNull();
      expect(root.querySelector('.breville-time')).toBeNull();
    }
  });

  it('does not present idle presets as live targets and formats each temperature with its own unit', async () => {
    const root = await renderFixture({
      status: 'idle',
      temperature: { state: '25', attributes: { unit_of_measurement: '°C' } },
      target_temperature: { state: '400', attributes: { unit_of_measurement: '°F' } },
      mode: 'bake',
    });
    expect(root.querySelector('.breville-current-temp')?.textContent).toContain('25 °C');
    expect(root.querySelector('.breville-target-temp')).toBeNull();
    expect(root.querySelector('.breville-mode')).toBeNull();
  });
});
