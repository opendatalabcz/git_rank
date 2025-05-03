# GitRank

<div align="center">

[![Build status](https://github.com/opendatalabcz/git_rank/workflows/build/badge.svg?branch=master&event=push)](https://github.com/opendatalabcz/git_rank/actions?query=workflow%3Abuild)
![Coverage Report](assets/images/coverage.svg)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/opendatalabcz/git_rank/blob/master/.pre-commit-config.yaml)
[![License](https://img.shields.io/github/license/opendatalabcz/git_rank)](https://github.com/opendatalabcz/git_rank/blob/master/LICENSE)

</div>

## Lokální instalace

1. Pokud nemáte nainstalované `Poetry`:

```bash
make poetry-download
```

nebo

```bash
pip install poetry
```

2. Instalace závislostí pomocí Poetry:

```bash
make install
```

3. Instalace potřebných linterů (je potřeba mít Java a .NET runtime):

```bash
make linters-install
```

4. Spuštění projektu:

```bash
./entrypoint.sh
```

## Proměnné prostředí (ENV)

Pro spuštění je potřeba mít definované následující proměnné prostředí (ve sloupci "Hodnota" jsou typické ukázkové hodnoty):

| Proměnná | Hodnota |
| :------- | :------ |
| SERVER_HOST | localhost |
| SERVER_PORT | 8090      |
| GITHUB_ACCESS_TOKEN | ghp_xyz |

## Template

Základní kostra projektu byla vygenerována z [python-package-template](https://github.com/TezRomacH/python-package-template).
