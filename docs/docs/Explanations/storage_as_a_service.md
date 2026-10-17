# Storage as a service

Storage bought from a cloud provider (block storage such as EBS, or any disk attached to an instance as a service) is evaluated with `POST /v1/storage`. It is separate from cloud instances: `ssd_storage` and `hdd_storage` on a cloud instance still only attribute disks inside the reference server.

## Request

```json
{
  "configuration": {
    "storage_type": "SSD",
    "capacity": 1000,
    "manufacturer": "Samsung",
    "replication": 1
  },
  "usage": {
    "storage": 2000,
    "hours_electrical_consumption": 12,
    "usage_location": "FRA"
  }
}
```

| Field | Description |
|---|---|
| `configuration.storage_type` | `SSD` or `HDD`. Object storage (S3 and similar) is not supported: the media behind it is not disclosed. |
| `configuration.capacity` | Capacity of the reference disk, in GB. Defaults to the archetype's disk capacity. |
| `configuration.manufacturer` | Used to complete the SSD density from the manufacturer dataset. |
| `configuration.replication` | Number of copies stored. Impact is multiplied by this value. |
| `usage.storage` | Amount of storage used, in GB. |
| `usage.hours_electrical_consumption` | Hours per day of use, mapped to `use_time_ratio` (hours / 24). Not used by the embedded impact. |
| `usage.usage_location` | Country code for the electricity mix. Not used by the embedded impact. |

## Method

Only the embedded impact is computed. For a reference disk of the same type:

```
impact = impact(reference disk) × (storage × replication / reference capacity)
```

The reference disk is built from the same archetype and factors as `POST /v1/component/ssd` or `/hdd`, so the per-GB value follows the disk model.

## HDD limitation

The HDD impact factor is flat: it does not depend on capacity (see `hdd_impact_embedded`). The per-GB value for HDD storage is therefore the reference disk's impact divided by the reference capacity, and the response carries a warning saying so. Results for HDD depend on the reference capacity chosen.

## Not yet covered

- Object storage (S3, Scaleway, etc.) and per-provider archetypes, until the replication factors are sourced.
- The use phase.
