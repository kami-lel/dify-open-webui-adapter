# dify-open-webui-adapter CHANGELOG

[^format]

<!-- todo support file uploads -->
















## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
















## [2.1.0] - 2026-01-07

### Added

- support for Chatflow in blocking and streaming mode
- support for Workflow in streaming mode

### Changed

- split up functionalities of OWU & Dify sides into different classes
















## [2.0.0] - 2026-01-04

### Added

- use **hooks-utility** for Git Hooks as Git Submodule

### Changed

- each adapter instance only supports single App now
- use constant in Python script for configuration, better config validation

### Fixed

- update format to fit updated Dify and Open WebUI

















## [1.1.0] - 2025-09-15

### Added

- support Dify Chatflow
- allow single adapter to support multiple Dify apps

### Fixed

- handle various errors
















## [1.0.0] - 2025-09-15

### Added

- basic single-round functionality













[unreleased]: https://github.com/kami-lel/kami-log-py/compare/v2.1.0...dev
[2.1.0]: https://github.com/kami-lel/kami-log-py/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/kami-lel/kami-log-py/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/kami-lel/kami-log-py/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/kami-lel/kami-log-py/releases/tag/v1.0.0













[^format]: CHANGELOG format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); Version scheme adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).