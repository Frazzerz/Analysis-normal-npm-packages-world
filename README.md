# npm Packages Analyzer

Python tool that computes file- and version-level metrics on npm package releases, developed for my Master's Thesis *"Metric-based Analysis to Identify Anomalous Releases in the npm Ecosystem Software Supply Chain"* (University of Genoa, DIBRIS).

- **Author:** Michele Frattini
- **Thesis repository:** [Thesis-Frattini-Metric-analysis-NPM](https://github.com/Frazzerz/Thesis-Frattini-Metric-analysis-NPM)

---

## What it does

The tool downloads the releases of one or more npm packages, extracts their tarballs, and analyzes every file they contain to compute, per version, the five metrics discussed in Chapter 6 of the thesis:

1. **File Types** — file type classification via [Magika](https://github.com/google/magika)
2. **Package Size** — uncompressed size in bytes of each file
3. **Longest Line Length** — computed on plain-text files after stripping comments (via [tree-sitter](https://tree-sitter.github.io/tree-sitter/))
4. **Unique Hexadecimal Values** — regex-based detection of hex tokens (e.g. obfuscated identifiers)
5. **Unique Ethereum Addresses** — regex-based detection of `0x`-prefixed 40-hex-character addresses

Packages and their versions are processed sequentially (oldest → newest) so that metric evolution across releases can be tracked, while file-level analysis within each version is parallelized with `multiprocessing`. Results are exported as CSV files, one row per analyzed version.

## Usage

```bash
python3 main.py --json <input_file>.json [--output DIR] [--workers N] [--log FILE] [--local] [--local-dir DIR] [--delete-analysis]
```

| Flag | Description |
|---|---|
| `--json` | **(required)** JSON file with the list of npm package names to analyze (see `list_pkg.json` for an example) |
| `--output` | Output directory for the results (default: `analysis_results`) |
| `--workers` | Number of parallel processes for per-file metric computation (default: number of CPU cores) |
| `--log` | Log file path (default: `log.txt`) |
| `--local` | Also include local tarballs, e.g. malicious releases no longer available on the registry |
| `--local-dir` | Directory containing the local tarballs (default: `./local_versions`) |
| `--delete-analysis` | Delete previous analysis results before running |

For each package, by default the tool downloads and analyzes its **20 most recent versions**. When `--local` is used, the 19 most recent legitimate versions are fetched from the registry and the 20th slot is filled with a local tarball (e.g. a compromised release retrieved separately) — this is how the goodware and malware datasets of the thesis were built.

Malicious tarballs no longer available on the official npm registry can be retrieved with the companion script [Download-malicious-npm-packages](https://github.com/Frazzerz/Download-malicious-npm-packages), then placed in the local versions directory and passed to this tool via `--local`.

## Repository structure

```
.
├── main.py                       # CLI entry point
├── analyze_single_package.py     # Orchestrates the analysis of one package
├── config.py                     # Paths and the list of metric columns exported to CSV
├── dataset.py                    # Dataset-building utilities
├── list_pkg.json                 # Example input file (list of package names)
├── analyzers/
│   ├── package_analyzer.py       # Coordinates registry + local versions for a package
│   ├── version_analyzer.py       # Analyzes all versions of a package
│   ├── local_version_analyzer.py # Handles local (offline) tarballs
│   ├── code_analyzer.py          # Per-file textual analysis (comments stripping, etc.)
│   ├── metrics_aggregator.py     # Aggregates per-file metrics into per-version metrics
│   └── categories/                # Metric-family analyzers (generic, evasion, crypto, exfiltration, payload)
├── models/
│   ├── code_type.py               # File/code type enumeration
│   ├── version_entry.py           # Data model for a package version
│   ├── domains/                   # Metric field definitions (generic, evasion, crypto, exfiltration, payload)
│   └── composed_metrics/          # Per-file and per-version aggregated metric models
├── reporters/
│   └── csv_reporter.py            # Flattens and writes results to CSV
└── utils/
    ├── npm_client.py              # Queries the npm registry, downloads and orders tarballs
    ├── file_handler.py            # Filesystem helpers (extraction, cleanup)
    ├── file_type_detector.py      # Wraps Magika for file-type classification
    └── logging_utils.py           # Thread-safe logging helpers
```

> Note: the codebase also defines additional metric domains (`exfiltration`, `payload`, extra `evasion`/`crypto` fields) left over from earlier experiments with metrics that were ultimately discarded from the thesis. They are not part of the columns currently exported (see `COLUMNS_TO_EXTRACT` in `config.py`), but they show how the tool is designed to be modular: adding a new metric generally just means extending the relevant domain model in `models/domains/`, adding its computation logic in `analyzers/categories/`, and listing the new field in `COLUMNS_TO_EXTRACT`.

## Requirements

The tool is written in Python 3 and relies on:

- [`requests`](https://pypi.org/project/requests/) — npm registry API calls and tarball downloads
- [`magika`](https://pypi.org/project/magika/) — deep-learning-based file type detection
- [`tree-sitter`](https://pypi.org/project/tree-sitter/) and [`tree-sitter-typescript`](https://pypi.org/project/tree-sitter-typescript/) — comment stripping for JS/TS files
- [`packaging`](https://pypi.org/project/packaging/) — semantic version parsing/sorting
- [`pandas`](https://pypi.org/project/pandas/) — post-processing of the exported datasets

```bash
pip install requests magika tree-sitter tree-sitter-typescript packaging pandas
```

## Related repositories

- 📄 **[Thesis-Frattini-Metric-analysis-NPM](https://github.com/Frazzerz/Thesis-Frattini-Metric-analysis-NPM)** — LaTeX sources of the Master's Thesis this tool was built for.
- 📥 **[Download-malicious-npm-packages](https://github.com/Frazzerz/Download-malicious-npm-packages)** — companion script to retrieve unpublished/compromised npm tarballs from mirror registries, used as input for the `--local` flag.
- 📊 **[Datasets-npm-Analysis](https://github.com/Frazzerz/Datasets-npm-Analysis)** — the goodware and malware datasets produced with this tool.
