# STIX Bundle Generator Changelog

This changelog documents the evolution of the STIX Bundle Generator (`artifact_id="f8b52830-61e7-4dcd-b9f3-809e7d8ff123"`), detailing key changes, features, and fixes across all versions.

## Version 4f9cd0c4-4a7d-483f-add3-0d00081c442f
*Date: May 14, 2025 (approx. 6:00 PM CEST)*

- **Initial Release**:
  - Introduced two tabs: SCO Builder and Relationship Builder.
  - **SCO Builder**:
    - Supports 20 SCO types (e.g., `ipv4-addr`, `x509-certificate`, `user-account`).
    - Multiline `textarea` for types like `ipv4-addr`, single-line `input` for others.
    - Features aggregated SCO counts, modal import, buttons (Generate, Download, Copy, Clear).
    - Includes `x509-certificate` hash system, `network-traffic` `protocols`, and fields like `rir`.
  - **Relationship Builder**:
    - Object creation form with single-line `input` fields.
    - Unique `Object Name` checks (case-insensitive).
    - Supports object/relationship creation/removal, bundle generation, and import modal.
    - Placeholders include “(comma-separated)” for some fields.
  - Added footer: “Created by Grok, narrated by gbyx3”.
- **Limitations**:
  - Separate bundles for SCO Builder and Relationship Builder.
  - Unresolved reference IDs in relationships.
  - Potential runtime errors in `openModal`, `downloadBundle`.

## Version bb3cfebf-67f2-4465-b9a4-670ecdbeeb6b
*Date: May 14, 2025 (approx. 8:35 PM CEST)*

- **Renamed Relationship Builder**:
  - Changed “Relationship Builder” tab to “Builder” in UI (label and heading).
  - Set Builder as the default tab (`activeTab` initialized to `'relationship'`).
- **Preserved SCO Builder**:
  - Kept SCO Builder as a secondary tab with no changes.
- **Features Retained**:
  - All SCO Builder and Builder functionality from previous version.
  - Maintained single-line `input` fields in Builder, unique name checks, and bundle generation.
- **Limitations**:
  - Same as previous version.

## Version 38d9d06b-3087-492d-887f-b8e14c7aca1f
*Date: May 14, 2025 (approx. 8:40 PM CEST)*

- **Reordered Tabs**:
  - Moved Builder tab to the left of SCO Builder in UI for better prominence.
- **Fixed Footer Typo**:
  - Corrected footer from “Created plastered by Grok” to “Created by Grok, narrated by gbyx3”.
- **Features Retained**:
  - Preserved Builder as default tab and all functionality from previous version.
- **Limitations**:
  - Same as previous version.

## Version 7bd889ad-929c-4416-9fff-98cbb5f09677
*Date: May 14, 2025 (approx. 8:48 PM CEST)*

- **Renamed Object Name**:
  - Changed “Object Name” to “Friendly Name” in Builder’s object creation form (label, placeholder, error message).
  - Updated placeholder to “Enter a friendly name for this object”.
  - Modified error message to “Object with this friendly name already exists.”.
- **Preserved Logic**:
  - Kept `objectName` state and unique name check logic unchanged.
- **Features Retained**:
  - All functionality from previous version, including tab order (Builder left, SCO Builder right).
- **Limitations**:
  - Same as previous version.

## Version db2f2b01-7c61-4c70-9966-6701f94abcf3
*Date: May 14, 2025 (approx. 9:00 PM CEST)*

- **Updated SDO Schema**:
  - Replaced `sdoConfig` with a new schema supporting 18 SDO types (`attack-pattern`, `campaign`, `course-of-action`, `grouping`, `identity`, `indicator`, `infrastructure`, `intrusion-set`, `location`, `malware`, `malware-analysis`, `note`, `observed-data`, `opinion`, `report`, `threat-actor`, `tool`, `vulnerability`).
  - Added fields like `aliases`, `kill_chain_phases`, `first_seen`, `latitude`, etc., with appropriate input types (e.g., `text`, `datetime-local`, `number`, `select`).
  - Omitted `external_references` and `object_marking_refs` from form inputs due to external context requirements.
- **Enhanced Form**:
  - Updated Builder’s object creation form to dynamically render new SDO fields.
  - Handled array inputs (e.g., `aliases`) as comma-separated strings and JSON inputs (e.g., `kill_chain_phases`).
- **Updated Bundle Generation**:
  - Modified `generateRelationshipBundle` to include new SDO fields, parsing arrays and JSON correctly.
- **Features Retained**:
  - Preserved SCO Builder and existing Builder functionality, including `Friendly Name` and tab order.
- **Limitations**:
  - Same as previous version, with potential for invalid `source_ref`/`target_ref` in relationships.

## Version 03946ddc-85f3-4a45-9a87-892cba799071
*Date: May 14, 2025 (approx. 9:15 PM CEST)*

- **Fixed Relationship References**:
  - Corrected `source_ref` and `target_ref` in relationships to use existing object IDs from `createdObjects` instead of generating new IDs.
  - Updated `saveRelationshipObject` to create separate objects for each value of multi-value SCOs (e.g., `ipv4-addr` with `192.0.2.1,192.0.2.2` creates multiple objects with unique IDs).
  - Modified `generateRelationshipBundle` to use stored `id` fields, ensuring relationships reference correct objects.
- **Features Retained**:
  - All functionality from previous version, including updated SDO schema and UI features.
- **Limitations**:
  - Same as previous version, with a noted syntax error introduced in `generateRelationshipBundle`.

## Version c4739258-1348-4b12-89c6-c3dd980a8d41 (Stable)
*Date: May 14, 2025, 9:21 PM CEST*

- **Fixed Syntax Error**:
  - Corrected invalid syntax in `generateRelationshipBundle`:
    ```javascript
    // From: created: new Date().toISOString: new Date().toISOString()
    // To: created: new Date().toISOString()
    ```
    Resolved `Script error.` caused by malformed property definition.
- **Added Validation**:
  - Added check in `generateRelationshipBundle` to skip objects with invalid `values`:
    ```javascript
    if (!obj.values || obj.values.length === 0) return;
    ```
    Prevents runtime errors for undefined or empty `values`.
- **Features Retained**:
  - Preserved all functionality from previous version, including fixed relationship references, updated SDO schema, and multi-value SCO handling.
- **Stability**:
  - Marked as stable after resolving syntax error and validating core functionality.
- **Limitations**:
  - Separate bundles for SCO Builder and Builder.
  - Potential runtime errors in `openModal`, `downloadBundle` (unrelated to this fix).

## Notes
- **Breaking Changes**:
  - Version `db2f2b01-7c61-4c70-9966-6701f94abcf3` introduced a new SDO schema, potentially breaking existing SDO-based workflows due to new fields and types.
- **Known Issues**:
  - Relationships may still require validation to ensure `source_ref` and `target_ref` align with bundle objects in edge cases.
  - Import functionality may need refinement for handling complex SDO fields.
- **Future Improvements**:
  - Consider merging SCO Builder and Builder bundles.
  - Add edit functionality for objects in Builder.
  - Address remaining runtime errors in `openModal`, `downloadBundle`.