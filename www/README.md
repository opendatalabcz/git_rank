# GitRank WWW

<div align="center">

[![Build status](https://github.com/opendatalabcz/git_rank/workflows/build/badge.svg?branch=master&event=push)](https://github.com/opendatalabcz/git_rank/actions?query=workflow%3Abuild)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/opendatalabcz/git_rank/blob/master/.pre-commit-config.yaml)
[![License](https://img.shields.io/github/license/opendatalabcz/git_rank)](https://github.com/opendatalabcz/git_rank/blob/master/LICENSE)

</div>

## Lokální instalace

1. Instalace Node.js závislostí:

```bash
npm install
```

2. Spuštění vývojového prostředí:

```bash
npm run dev
```

## Proměnné prostředí (ENV)

Pro spuštění je potřeba mít definované následující proměnné prostředí (ve sloupci "Hodnota" jsou typické ukázkové hodnoty):

| Proměnná | Hodnota |
| :------- | :------ |
| VITE_GIT_RANK_API_URL | http://localhost:8090 |

## Template

Základní kostra projektu byla vygenerována z Vite šablony [react-ts](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts).
