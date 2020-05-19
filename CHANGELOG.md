# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- `Auth` object
- `Device` object
- `Card` endpoint
- `Payment.auth` property
- `Payment.date_bank` property
- `Payment.device` property
- `Payment.fee` property
- `Payment.return_url` property
- `Payment.unique_id` property
- `Payment.payment_page_url()` method
- `Customer.external_id` property
- `Card.funding` property
- `Card.nature` property
- `Card.network` property

### Changed
- `Object.save()` is renamed `Object.send()`
- `AuthStatus`, `PaymentStatus` and `RefundStatus` use python's native `Enum`
- `Payment.status` can be modified
- `Object.send()` can be use without method
- `Object.hydrate()` will use setter when possible
- `Payment.is_success` and `Payment.is_error` are based on `Payment.status` now
- `Payment.order_id` accept 36 characters
- `IliadHTTPError.factory()` replaced by `IliadHTTPError.__new__()`
- Simplify datetime property management

### Fixed
- All datetime will be "aware" and use UTC as default
- `Object.created` can be call directly on new instances (and fetch the API is possible)
- Exceptions will use standard Python message mechanism (aka `str(err)`)
- `Object.to_json()` will not send empty object
- Populated flag are passed to inner object
- Reseting modified flag will trigger a reset on inner object too


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
