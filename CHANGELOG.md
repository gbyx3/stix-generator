# Changelog for STIX Bundle Generator (index.html)

All notable changes to the `index.html` artifact (`artifact_id="f8b52830-61e7-4dcd-b9f3-809e7d8ff123"`) are documented in this file. Versions are listed in descending order, with the latest version at the top.

## [Stable] Version 92386760-6add-4294-bbdf-4b3b40b4fe62 - 2025-05-19 20:25 CEST
- **Fixed**: Corrected syntax error in `generateBundle` function, changing `if (key.includes('.' yok))` to `if (key.includes('.'))`, resolving the "Script error." runtime issue.
- **Meta**: Updated `<meta name="xaiArtifact_version">` to `e6f4c2b3-9d5e-4c3a-8f1d-9a8b7c6d5e0f`.
- **Notes**: Marked as stable. Preserved all functionality, including `goals` for `threat-actor`, relationship constraints, and SCO nesting.

## Version 7bda4770-1c15-4f92-9978-155f7e71fa11 - 2025-05-19 20:21 CEST
- **Added**: `goals` property to `threat-actor` SDO, with a text input for comma-separated values (e.g., `Financial Gain, Espionage`) in `sdoConfig`.
- **Updated**: `generateBundle` to process `goals` as a list of strings for `threat-actor`.
- **Updated**: `handleBundleImport` to join `goals` as a comma-separated string for `threat-actor` imports.
- **Meta**: Updated `<meta name="xaiArtifact_version">` to `d5e3b1a2-8c4f-4d3b-9e2c-7f8a6b5c4d0e`.
- **Notes**: Ensured STIX 2.1 compliance for `goals` and preserved relationship constraints and SCO nesting.

## Version 1301525f-336a-47eb-81a0-9f95f3a4756c - 2025-05-19 20:11 CEST
- **Added**: Relationship constraints based on provided JSON, restricting source SDOs (`indicator`, `malware`, etc.), target SDOs, and relationship types (`attributed-to`, `indicates`, `related-to`).
- **Updated**: Source Object `<select>` to show only eight allowed SDOs.
- **Updated**: Target Object `<select>` to filter based on source’s `allowed_targets`.
- **Updated**: Relationship Type `<select>` to filter based on source and target constraints.
- **Updated**: `saveRelationship` to validate relationships, showing alerts for invalid combinations.
- **Meta**: Updated `<meta name="xaiArtifact_version">` to `c4f9b2a1-7d3e-4b2a-9c1d-8e7f6a5b3c4f`.
- **Notes**: Enhanced UI to disable invalid selections and preserved SCO nesting and import validation.

## Version da3a23b9-119b-460a-acc5-40ef8fd13739 - 2025-05-19 19:49 CEST
- **Fixed**: Enabled `observed-data` selection in relationship dropdowns by creating `observed-data` SDOs for SCOs in `saveObject`.
- **Updated**: `saveObject` to store `observed-data` wrappers in `createdObjects` with nested SCOs.
- **Updated**: `generateBundle` to use `observed-data` SDOs from `createdObjects`.
- **Updated**: Relationship `<select>` to include `observed-data` (removed exclusion filter).
- **Meta**: Updated `<meta name="xaiArtifact_version">` to `b4e2c1f7-9a3d-4e8b-a2c9-fd7a6e5b3c4f`.
- **Notes**: Supported relationships like `indicator` → `indicates` → `observed-data` and maintained STIX 2.1 compliance.

## Version da7f8258-086e-45fe-9d8a-e581563447a0 - 2025-05-16 15:22 CEST
- **Fixed**: Removed `observed-data` from relationship dropdowns (Source/Target Object `<select>`) to prevent its use as a relationship object, as it was incorrectly included.
- **Meta**: Updated `<meta name="xaiArtifact_version">` to `7a9c3b2e-8f4d-4c2a-b3e1-5f6e7d8f9a0b`.
- **Notes**: Assumed `observed-data` was only a SCO container, later corrected to allow relationships. Preserved SCO nesting and other functionality.

## Version d3df6462-c36e-424a-bf19-d63ccfb6634a - 2025-05-16 14:03 CEST
- **Fixed**: Ensured `number_observed` in `observed-data` is an integer ≥ 1 (default `1`), preventing `null` values.
- **Fixed**: Removed `id` and `spec_version` from SCOs nested in `observed-data.objects`, per STIX 2.1 requirements.
- **Updated**: `generateBundle` to enforce these constraints.
- **Updated**: `handleBundleImport` to validate `number_observed` and SCO properties during import.
- **Meta**: Updated `<meta name="xaiArtifact_version">` to `9e6a7b8c-2d3e-4f1a-9c2b-3f4e5d6f7890`.
- **Notes**: Strengthened STIX 2.1 compliance for SCO nesting and `observed-data` properties.

## Version e03a3cd9-5948-444a-aac3-fe2ae2e6be07 - 2025-05-16 14:03 CEST
- **Added**: SCO nesting in `observed-data` SDOs, ensuring no top-level SCOs in the bundle.
- **Added**: Auto-wrapping of SCOs in `observed-data` with `first_observed`, `last_observed`, and `number_observed`.
- **Added**: SCO-to-SCO relationships via references (e.g., `contains_ref`, `creator_user_ref`) in SCO properties.
- **Updated**: `generateBundle` to wrap SCOs in `observed-data` and restrict top-level objects to SDOs and relationships.
- **Updated**: `saveRelationship` to allow only SDO-to-SDO relationships, using references for SCOs.
- **Updated**: `handleBundleImport` to reject bundles with top-level SCOs.
- **Updated**: UI with a note indicating SCOs are wrapped in `observed-data`.
- **Meta**: Updated `<meta name="xaiArtifact_version">` to `9e6a7b8c-2d3e-4f1a-9c2b-3f4e5d6f7890`.
- **Notes**: Consolidated to a single Builder interface, removed SCO Builder tab, and preserved `optgroup` labels.

## Version 380d42b4-f491-4f8b-b825-df384aafdc08 - 2025-05-16 (Time not specified)
- **Initial Version**: Implemented the STIX Bundle Generator as a single-page React application.
- **Features**:
  - Supported creation of 20 SCO types and 18 SDO types with dynamic input fields.
  - Included `optgroup` labels ("Cyber Object Types", "Domain Object Types") in object type `<select>`.
  - Enabled SDO-to-SDO relationship creation with basic validation.
  - Supported bundle generation, download, and import with a modal interface.
  - Used Tailwind CSS for styling and Babel for JSX transpilation.
- **Meta**: `<meta name="xaiArtifact_version">` set to `380d42b4-f491-4f8b-b825-df384aafdc08`.
- **Notes**: Initial implementation lacked SCO nesting constraints and advanced relationship validation. Specific timestamp not provided in history.

---

**Notes**:
- All versions maintain STIX 2.1 compliance, with progressive enhancements to enforce SCO nesting, relationship constraints, and property validation.
- Timestamps are based on the provided conversation history, with the earliest version lacking a specific time.
- The changelog assumes all listed `artifact_version_id` values from the history are included; if earlier versions exist, they were not provided.
- For further details on any version, refer to the corresponding `index.html` artifact.