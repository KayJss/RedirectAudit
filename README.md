# RedirectAudit

Small CLI for finding redirect-chain problems after domain, HTTPS, reverse-proxy, route or SEO changes.

## Features
- Displays 301/302/303/307/308 hops
- Resolves relative Location headers
- Detects redirect loops
- Flags chains with 5+ redirects
- Reports broken final HTTP status
- JSON output and CI-friendly exit codes
- Configurable maximum hop count
- Zero third-party runtime dependencies

## Install
```bash
python -m pip install -e .
```

## Usage
```bash
redirectaudit https://example.com
redirectaudit https://example.com --json
redirectaudit https://example.com --max-hops 15
```

## Tests
```bash
python -m unittest discover -s tests -v
```

`redirectaudit/core.py` contains validation and analysis. `redirectaudit/cli.py` performs hop-by-hop requests and CLI output.

Useful for HTTP-to-HTTPS migrations, old-domain migrations, reverse-proxy loop checks and post-deploy URL sanity checks.

## License
Proprietary / All Rights Reserved. See `LICENSE`.
