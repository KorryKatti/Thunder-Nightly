# Thunder-Nightly

**Thunder-Nightly** is the development/nightly version of [github.com/korrykatti/thunder](https://github.com/korrykatti/thunder). Features are tested and refined here before being merged into the stable release.

A modern, intuitive desktop application launcher for open-source Python programs hosted on GitHub.

## About

Thunder-Nightly allows users to:
- Browse open-source Python applications from GitHub
- Download and install apps with one click
- Manage updates seamlessly
- Launch and run Python apps directly from the desktop
- Organize your app library

Think of it as a curated launcher for the Python open-source ecosystem.

## Inspiration

Thunder was inspired by [this Reddit discussion](https://www.reddit.com/r/github/comments/1at9br4/i_am_new_to_github_and_i_have_lots_to_say/?share_id=PgaydUZlRDobIywviJrnb&utm_medium=android_app&utm_name=androidcss&utm_source=share&utm_term=1).

## Project Status

**Current Development Phase**: Client Application (Desktop UI + Local Features)

- **Last Significant Update**: May 28, 2025 (Flask backend)
- **Current Focus**: Transitioning to **Wails** (Go) + Vanilla HTML/CSS/JS
- **Progress**: Planning & Architecture (See [plan.md](plan.md) for detailed roadmap)

## Architecture

### Tech Stack
- **Frontend**: Vanilla HTML/CSS/JavaScript (works offline without UI breaking)
- **Desktop Framework**: [Wails](https://wails.io/) (Go backend)
- **Data Storage**: JSON-based local storage (~/.thunder-nightly/)
- **Package Management**: GitHub API integration

### Language Support
Currently focuses on Python applications. Support for additional languages (Node.js, Rust, etc.) can be added in future versions based on user demand.

## Roadmap

### Phase 1: Foundation (In Progress)
- [ ] Wails project initialization
- [ ] GitHub API integration
- [ ] App download/install mechanism
- [ ] Local app storage system

### Phase 2: UI & UX
- [ ] Desktop app interface
- [ ] Store/Browse view
- [ ] Library management view
- [ ] App execution & management

### Phase 3: Core Features
- [ ] Python app execution
- [ ] Version management & updates
- [ ] App configuration options
- [ ] User preferences

### Phase 4+: Polish & Advanced
- [ ] Performance optimization
- [ ] Cross-platform testing
- [ ] Quality of life features
- [ ] Long-term sustainability


## Development Note

Thunder-Nightly was previously built with Flask (Python backend). We're transitioning to:
- **Wails** for better desktop integration
- **Go** for improved performance
- **Vanilla JavaScript** for minimal dependencies

This provides a solid foundation for the stable Thunder release.

## Code of Conduct

This project adheres to the Contributor Covenant. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## License

See [LICENSE](LICENSE) for license information.

---

**Related Projects**: [github.com/korrykatti/thunder](https://github.com/korrykatti/thunder)
