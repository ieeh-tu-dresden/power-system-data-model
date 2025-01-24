## 2.3.2 (2025-01-24)

### Fix

- **ci**: release workflow (#162)
- add py.typed marker (#160)

## 2.3.1 (2024-08-23)

### Fix

- add tests for AttributeData initialization (#141)
- extend BranchType for series assets (RLC) (#144)

## 2.3.0 (2024-08-01)

### Feat

- add possibility for optional meta information (#127)
- validate topology case (contributors: @SebastianDD)

### Fix

- **erdantic**: pin erdantic `<1` (#136)
- use platform dependent max. size for `UniqueNonEmptyTuple` (#131)
- rename `is_valid_topology` to `matches_topology` (#130)

## 2.2.0 (2024-02-14)

### Feat

- extend Meta with attribute `creator` (contributors: @SebastianDD)

### Fix

- remove constraints for value of Impedance and Admittance (contributors: @SebastianDD)

## 2.1.2 (2024-02-08)

### Fix

- add `p_set` for `ControlPF` (contributors: @SebastianDD)
- freeze `pydantic` version to 2.5.3 (contributors: @SebastianDD, @sasanjac)
- add default `system_type` for Length (contributors: @SebastianDD)

## 2.1.1 (2023-12-19)

### Fix

- allow NaN for powerfactor import (contributors: @sasanjac, @SebastianDD)

## 2.1.0 (2023-12-06)

### Feat

- rework quantity rounding (contributors: @sasanjac, @SebastianDD)
- specify system for quantities (contributors: @sasanjac, @SebastianDD)

## 2.0.1 (2023-11-01)

### Fix

- release pipeline

## 2.0.0 (2023-11-01)

### BREAKING CHANGE

- remove `meta.name` (contributors: @sasanjac)
- remove `phase_connection_type` (contributors: @sasanjac)
- add phase connections to external grid (contributors: @sasanjac)

### Feat

-  add earth and additional phase options (contributors: @sasanjac, @SebastianDD)

### Fix

- use n-phase quantities consistently (contributors: @sasanjac, @SebastianDD)
- disallow empty sequences for quantity values (contributors: @sasanjac)

## 1.9.0 (2023-10-25)

### Feat

- use n-phase quantities instead of single floats (contributors: @sasanjac, @SebastianDD)

### Fix

- deprecate meta.name in favor of meta.grid (contributors: @SebastianDD, @sasanjac)
- add reference voltage to load model (contributors: @sasanjac, @SebastianDD)

## 1.8.1 (2023-09-20)

### Fix

- export version attribute in metadata using pydantic v2 (contributors: @sasanjac)

## 1.8.0 (2023-09-19)

### Feat

- rework power calculation in steadystate case (contributors: @SebastianDD, @sasanjac)
- add meta attr sign convention (contributors: @SebastianDD)

## 1.7.0 (2023-09-05)

### Feat

- add support for constant-impedance and -current loads (contributors: @sasanjac)

### Fix

- make all zero sequence attributes of transformer optional (contributors: @SebastianDD)

## 1.6.0 (2023-08-29)

### Feat

- add more load and system types
- add case field to meta information

### Fix

- reenable unique constraints on object lists
- allow only technically possible transformer vector groups
- add zero sequence magnetisation information
- add vectorgroup "YNyn5"

## 1.5.1 (2023-07-25)

### Fix

- missing control type information in controller

## 1.5.0 (2023-07-06)

### Feat

- Python 3.11 support

### Fix

- migrate to pydantic v2.0
- add `is_symmetrical` to `RatedPower`
- zenodo doi

## 1.4.0 (2023-06-27)

### Feat

- assign connected phases for each load component
- add support for fuse types
- type of  `RatedPower` must be specified (contributors: @sasanjac)

### Fix

- zenodo reference (contributors: @SebastianDD)

## 1.3.1 (2023-05-23)

### Fix

- correct numeric types (contributors: @sasanjac)

## 1.3.0 (2023-05-05)

### Feat

- add link to zenodo (contributors: @SebastianDD)
- add neutral conductor information (contributors: @SebastianDD, @sasanjac)

### Fix

- add neutral phase to load (contributors: @sasanjac)
- add missing transformer vector groups (contributors: @SebastianDD)

## 1.2.0 (2023-03-20)

### Feat

- isolate schema
