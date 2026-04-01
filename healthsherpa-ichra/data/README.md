# ICHRAverse Data Files

## Schema

### states.json
| Field | Type | Description |
|-------|------|-------------|
| code | string | 2-letter state code |
| name | string | Full state name |
| employers | number | Employers using ICHRA |
| covered_lives | number | Total covered lives |
| yoy_growth_pct | number | Year-over-year growth % |
| carriers_active | number | Active carriers in state |
| platforms_active | number | Active platforms in state |
| market_stage | string | nascent / early_growth / accelerating / leading |
| data_note | string | Data provenance note |

### carriers.json
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier |
| name | string | Carrier display name |
| states | array | State codes where active |
| ichra_status | string | active / exploring / not_started |
| hs_connected | boolean | Connected to HealthSherpa platform |

### platforms.json
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier |
| name | string | Platform display name |
| states | array | State codes where active |
| hs_connected | boolean | Connected to HealthSherpa |

## Switching to Live Data

All files in this directory are **sample data** for demonstration purposes.

To connect live HealthSherpa data:
1. In `map/index.html`, change `CONFIG.dataSource` from `"mock"` to `"live"`
2. Set `CONFIG.liveApiEndpoint` to the HealthSherpa ICHRA API endpoint
3. For security, route API calls through a Netlify serverless function proxy — never expose API keys in client-side code
4. Ensure the live API returns JSON matching the schema above
