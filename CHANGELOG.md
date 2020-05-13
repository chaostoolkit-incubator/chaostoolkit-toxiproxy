# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-toxiproxy/compare/0.2.1...HEAD

### Added

- Use `toxiproxy_url` for defining toxiproxy-api base URL.

## [0.2.1][]

[0.2.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-toxiproxy/compare/0.2.0...0.2.1

### Added

- Build Python 3.7 too
- Specify readme format for Pypi

## [0.2.0][]

[0.2.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-toxiproxy/compare/0.1.3...0.2.0

### Changed

- Fixed modify_proxy action: Does not error on a successful call and returns proper error message
- Add support for [reset endpoint](https://github.com/Shopify/toxiproxy#endpoints)

## [0.1.3][]

[0.1.3]: https://github.com/chaostoolkit-incubator/chaostoolkit-toxiproxy/compare/0.1.2...0.1.3

### Changed

-   delint
-   use the appropriate typing annotation `Any` instead of `any` which is a builtin
    function

## [0.1.2][]

[0.1.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-toxiproxy/compare/0.1.1...0.1.2

Just so that we can re-upload to Pypi...

## [0.1.1][]

[0.1.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-toxiproxy/compare/0.1.0...0.1.1

### Added

-   add `MANIFEST.in` for building a proper Python distribution package

## [0.1.0][]

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-toxiproxy/compare/51c126...0.1.0

### Changed

-   Module name to `chaostoxi`

### Added

-   Travis CI
-   Initial version of code
