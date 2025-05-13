# CHANGELOG

All notable changes to the STIX Bundle Generator project are documented in this file.

## [ebba5370-9bc3-48d0-b86f-4980f40a4ba8] - 2025-05-13
- **Fixed**: Updated "Added SCOs" section to aggregate SCOs by type, displaying one chip per type with the total count (e.g., `user-account (2)` for two `user-account` SCOs). Clicking a chip edits the last SCO of the type; the remove button deletes the last SCO.
- **Preserved**: Single-line `input` for primary fields and `windows-registry-key` `values`, single-value submission, and all existing features (20 SCO types, clickable chips, modal import, buttons, `x509-certificate` hash system, `network-traffic` `protocols` flat array, footer, placeholder).

## [772b9c0f-8afd-496f-8d88-301cb5c514e6] - 2025-05-13
- **Changed**: Replaced `textarea` with single-line `input` for primary fields of all non-`x509-certificate` SCOs and for `windows-registry-key` `values` field (previously `textarea`). Restricted submissions to one value at a time by processing `currentValues` as a single value in `saveSco`.
- **Preserved**: Modal import button labeled "Import", all existing features, and limitations (duplicate SCOs, IDs for `from_ref`/`src_ref`/`dst_ref`, potential runtime errors).

## [b6cd1f48-f490-447e-8168-28ed3e504707] - 2025-05-13
- **Changed**: Updated "Import STIX Bundle" button text to "Import" and its `aria-label` to "Import" for accessibility.
- **Preserved**: Reverted functionality from `9c4dc825-1f6b-4b68-a9d3-4405ee391a39`, including 20 SCO types, clickable chips, modal import, "Generate STIX Bundle", "Download JSON", "Copy to Clipboard", "Clear All SCOs", `x509-certificate` hash system, `network-traffic` `protocols` flat array, footer, and "Select SCO Type" placeholder.

## [cc452bb9-5cb3-4707-a446-8106fa23aa81] - 2025-05-13
- **Fixed**: Eliminated duplicate `email-addr`, `ipv4-addr`, and `ipv6-addr` SCOs in `handleBundleImport` by consolidating SCO addition with a `seenValues` `Map`, ensuring one SCO per unique `value`. Integrated reference processing (`from_ref`, `src_ref`, `dst_ref`) within the main SCO loop.
- **Preserved**: Single-line `input` changes, single-value submission, `ErrorBoundary`, standardized `onClick` handlers, and all existing features.
- **Note**: Introduced issues (unspecified breakage), leading to reversion request.

## [cf6a0e46-ea55-4d6d-867a-96be922c4cfa] - 2025-05-13
- **Fixed**: Attempted to fix duplicate `email-addr`, `ipv4-addr`, and `ipv6-addr` SCOs using a `seenValues` `Map` to track unique `value`s. Added checks for `from_ref`, `src_ref`, and `dst_ref` references.
- **Issue**: Duplicates persisted due to separate reference processing adding SCOs already present.
- **Preserved**: `ErrorBoundary`, standardized `onClick` handlers, single-line `input` for primary fields, and all existing features.

## [ffb7bdd2-7ace-480d-9bb1-a2188cbcd222] - 2025-05-13
- **Fixed**: Resolved `downloadBundle is not defined` error by changing `onClick={downloadBundle}` to `onClick={() => downloadBundle()}`.
- **Changed**: Standardized all button `onClick` handlers to use arrow functions (e.g., `onClick={() => functionName()}`) for consistency and to prevent binding issues.
- **Preserved**: `network-traffic` `src_ref`/`dst_ref`, `email-message` `from_ref`, `ErrorBoundary`, and all existing features.

## [149acdb2-c760-4b0d-abb5-c7f0dfac92ce] - 2025-05-13
- **Fixed**: Corrected `network-traffic` `src_ref`/`dst_ref` to display IP addresses in UI and ensure `ipv4-addr`/`ipv6-addr` SCOs appear as chips in "Added SCOs".
- **Fixed**: Resolved `openModal is not defined` error by changing `onClick={openModal}` to `onClick={() => openModal()}` and added `ErrorBoundary` for runtime error logging.
- **Preserved**: `email-message` `from_ref`, `network-traffic` `protocols` flat array, and all existing features.

## [464239f7-4610-4205-8be5-0902c1ea5ed4] - 2025-05-13
- **Fixed**: Attempted to fix `network-traffic` `src_ref`/`dst_ref` to display IP addresses in UI and add `ipv4-addr`/`ipv6-addr` SCOs as chips.
- **Issue**: IDs appeared in UI instead of IPs, and IP SCOs were inconsistent.
- **Preserved**: `email-message` `from_ref` and existing features.

## [81903165-62e7-4665-88a5-4a5d2ed56627] - 2025-05-13
- **Fixed**: Implemented `email-message` `from_ref` to link to `email-addr` SCO `value`, creating new SCOs if unmatched.
- **Preserved**: "Copy to Clipboard", "Clear All SCOs", and existing features.

## [9c4dc825-1f6b-4b68-a9d3-4405ee391a39] - 2025-05-13
- **Added**: "Copy to Clipboard" and "Clear All SCOs" buttons to the right of "Download JSON", styled with flex layout using Tailwind CSS.
- **Preserved**: `network-traffic` `protocols` flat array and existing features.

## [01f1622a-384b-4172-959a-995c37fb10c6] - 2025-05-13
- **Fixed**: Corrected `network-traffic` `protocols` to use a flat array (e.g., `["tcp"]` instead of `[["tcp"]]`) for consistent bundle generation.
- **Preserved**: Additional fields support and existing features.

## [100639cd-4026-4e92-95f7-1403cbca6c5c] - 2025-05-13
- **Added**: Support for additional fields: `rir`, `is_multipart`, `date`, `start`, `end`, `is_active`, `name`, `cpe`.
- **Added**: Checkbox inputs for `is_multipart` and `is_active`.
- **Preserved**: Modal import, clickable chips, and existing features.

## [d733fdab-a40a-415b-97e9-1ece70ab4be9] - 2025-05-13
- **Changed**: Made "Select SCO Type" a non-selectable placeholder using `<option value="" disabled selected hidden>`.
- **Preserved**: Footer and existing features.

## [b35784fe-25a2-4659-abed-ba0389716ec3] - 2025-05-13
- **Added**: Footer: "Created by Grok, narrated by gbyx3".
- **Preserved**: Clickable SCO chips and modal import.

## [98e45612-8ee9-4fd6-8efa-5ae1ac2d9d47] - 2025-05-13
- **Added**: Restored "Generate STIX Bundle" button.
- **Added**: Clickable SCO chips for editing and modal-based JSON import.
- **Preserved**: Basic SCO type support and bundle generation.

## [685f2bac-c859-4ec9-886b-f75e9279dbb6] - 2025-05-13
- **Initial Version**: Early implementation with non-clickable SCO chips and file-based import (not modal-based).
- **Note**: Served as a fallback reversion option.

---

**Note**: Dates are standardized to May 13, 2025, based on the project timeline. Each version preserves features from prior versions unless explicitly modified. Limitations in earlier versions (e.g., duplicate SCOs, unresolved `from_ref`/`src_ref`/`dst_ref`, runtime errors) were addressed in later versions but may persist in reverted states.