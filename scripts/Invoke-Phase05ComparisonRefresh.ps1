[CmdletBinding()]
param(
    [string[]]$Cases,
    [switch]$SkipChart,
    [switch]$SkipDiffCleanup,
    [switch]$ExportSlide
)

function Invoke-Phase05ComparisonRefresh {
    <#
        .SYNOPSIS
        Refreshes the Phase 05 · Step 03 SQL vs pandas evidence with one command.

        .DESCRIPTION
        Ensures the dockerized Python/PostgreSQL stack is running, reloads `books_clean`,
        runs the SQL vs pandas comparison CLI, and regenerates the plotted summary chart.
        Optionally limits the comparison to a subset of cases or skips chart creation.

        .PARAMETER Cases
        Optional list of comparison case identifiers (for example `M1_top_authors_by_weighted_rating`).
        Defaults to all registered cases when omitted.

        .PARAMETER SkipChart
        Skips the matplotlib chart refresh while still loading data and running the CLI.

        .PARAMETER SkipDiffCleanup
        Leaves any previously generated `*_differences.csv` files untouched.

        .PARAMETER ExportSlide
        Generates `docs/phase-05-step-03-task-01-slide.pptx` after the comparison run (requires chart output).

        .EXAMPLE
        PS> .\scripts\Invoke-Phase05ComparisonRefresh.ps1
        Reloads `books_clean`, runs all comparisons, and regenerates the PNG chart.

        .EXAMPLE
        PS> .\scripts\Invoke-Phase05ComparisonRefresh.ps1 -Cases M1_top_authors_by_weighted_rating -SkipChart
        Refreshes only the selected case and keeps the previous chart on disk.
    #>
    $ErrorActionPreference = 'Stop'
    $repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
    $composeArgs = @('compose', '-f', 'docker-compose.python.yml', '-f', 'docker-compose.postgresql.yml')

    Push-Location $repoRoot
    try {
        Write-Host 'Ensuring docker compose stack is up...' -ForegroundColor Cyan
        & docker @composeArgs 'up' '-d' | Out-Null

        if (-not $SkipDiffCleanup) {
            Write-Host 'Cleaning previous *_differences.csv artifacts...' -ForegroundColor Cyan
            Get-ChildItem 'outputs/phase05_step03_task01' -Filter '*_differences.csv' -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
        }

        Write-Host 'Loading books_clean into PostgreSQL...' -ForegroundColor Cyan
        & docker @composeArgs 'run' '--rm' 'app' 'python' '-m' 'src.load_books_clean_to_postgres' `
            '--csv-path' 'data/derived/books_clean.csv' '--table' 'books_clean' '--if-exists' 'replace'

        Write-Host 'Running SQL vs pandas comparison CLI...' -ForegroundColor Cyan
        $compareCommand = @($composeArgs + @('run', '--rm', 'app', 'python', '-m', 'src.analyses.portfolio.p04_sql_vs_pandas_compare', '--log-level', 'INFO', '--output-dir', 'outputs/phase05_step03_task01'))
        if ($Cases -and $Cases.Count -gt 0) {
            $compareCommand += '--cases'
            $compareCommand += $Cases
        }
        & docker @compareCommand

        if (-not $SkipChart) {
            Write-Host 'Regenerating comparison_summary.png chart...' -ForegroundColor Cyan
            & docker @composeArgs 'run' '--rm' 'app' 'python' '-m' 'src.analyses.support.storytelling.plot_comparison_summary' `
                '--input' 'outputs/phase05_step03_task01/comparison_summary.csv' `
                '--output' 'outputs/phase05_step03_task01/comparison_summary.png'
        }

        if ($ExportSlide) {
            Write-Host 'Exporting presentation slide deck...' -ForegroundColor Cyan
            & docker @composeArgs 'run' '--rm' 'app' 'python' '-m' 'src.analyses.support.storytelling.export_phase05_slide' `
                '--notes' 'docs/phase-05-step-03-task-01-notes.md' `
                '--summary-csv' 'outputs/phase05_step03_task01/comparison_summary.csv' `
                '--chart' 'outputs/phase05_step03_task01/comparison_summary.png' `
                '--output' 'docs/phase-05-step-03-task-01-slide.pptx'
        }

        Write-Host 'Phase 05 comparison refresh completed successfully.' -ForegroundColor Green
    }
    finally {
        Pop-Location
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    Invoke-Phase05ComparisonRefresh @PSBoundParameters
}
