# GitRank

<div align="center">

[![Build status](https://github.com/opendatalabcz/git_rank/workflows/build/badge.svg?branch=master&event=push)](https://github.com/opendatalabcz/git_rank/actions?query=workflow%3Abuild)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/opendatalabcz/git_rank/blob/master/.pre-commit-config.yaml)
[![License](https://img.shields.io/github/license/opendatalabcz/git_rank)](https://github.com/opendatalabcz/git_rank/blob/master/LICENSE)

</div>

GitRank je software sloužící k analýze a hodnocení uživatelské práce ve veřejných repozitářích (aktuálně z platformy GitHub) a následnému zobrazování výsledných reportů.

Poskytuje tak vhled na dovednosti a návyky vývojářů, které nemusí být na první pohled patrné.

## Struktura projektu

### git_rank

Obashuje samotnou rankovací aplikaci. Je napsána v Pythonu za pomocí FastAPI a je koncipována jako REST API. Generuje reporty v JSON formátu.

### www

Obsahuje přidruženou webovou stránku, pomocí které je možné Git Rank REST API zavolat, počkat na vygenerování JSON reportu, který webová stránka zobrazí v čitelnější podobě společně s dalšími vizualizacemi v podobě grafů.

## Spuštění projektu

Pro spuštění obou částí projektu je doporučeno využít připravený <code>docker-compose.yml</code>.

Pro sestavení images se všemi potřebnými závislostmi jsou využity příslušné <code>Dockerfile</code> uvnitř <code>www/docker</code> a <code>git_rank/docker</code> adresářů.

Pro spuštění REST_API je potřeba mít v adresáři <code>git_rank/</code> vytvořený příslušný <code>.env</code> soubor alespoň s <code>GITHUB_ACCESS_TOKEN</code> proměnnou, případně ji do <code>docker-compose.yml</code> přidat manuálně.

## Lokální instalace a spuštění

Pro variantu lokální instalace a spuštění je detail popsán v příslušných <code>README.md</code> souborech v adresářích jednotlivých komponent (<code>git_rank/</code> a <code>www/</code>).

Pro spuštění hodnoticí komponenty je potřeba mít nainstalovaný Python (alespoň 3.11) a pro webovou stránku Node.js (s npm). Popis instalace všech ostatních potřebných závislostí je součástí zmiňovaných README souborů.

## Dokumentace REST API

Dokumentace jednotlivých dostupných REST API endpointů je po spuštění dostupná na endpointu <code>/docs</code>.