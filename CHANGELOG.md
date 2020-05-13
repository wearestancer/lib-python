# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- `Auth` object
- `Device` object
- `Payment.auth` property
- `Payment.device` property
- `Payment.return_url` property
- `Payment.payment_page_url()` method

### Changed
- `Object.save()` is renamed `Object.send()`
- `Object.send()` can be use without method
- `Object.hydrate()` will use setter when possible


## [0.0.2] - 2020-03-18

### Added
- Refunds
- Allow `kwargs` at instance creation
- Default time zone configuration

### Changed
- `Object.hydrate()` use now `kwargs`
- `Object.to_json()` will export only modified values
- Better key management
- Add exceptions raised to docstring
- Remove typing from docstring

### Fixed
- Coverage regression test
- `Object.to_json()` may export an incorrect `id` field


## [0.0.1] - 2019-06-29

### Added
- First implementation
