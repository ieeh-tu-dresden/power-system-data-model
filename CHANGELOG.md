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
