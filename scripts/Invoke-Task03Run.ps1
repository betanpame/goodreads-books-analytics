function Invoke-Task03Run {
    <#
        .SYNOPSIS
        Runs one or more Phase 05 · Step 02 · Task 03 SQL scripts inside Docker using the documented compose/psql command.

        .DESCRIPTION
        Provides a single entry point for executing the Task 03 analysis scripts (`60_`, `70_`, `80_`).
        Accepts script identifiers or friendly aliases, ensures Docker Compose uses both stack files,
        and streams the `psql` output with `PAGER=cat` and `ON_ERROR_STOP=1` enabled.

        .PARAMETER Script
        One or more script identifiers. Accepts values `60`, `70`, `80`, `authors`, `publishers`, `rolling`, or `all`.
        Defaults to `all`.

        .EXAMPLE
        PS> .\scripts\Invoke-Task03Run.ps1 -Script 70
        Runs only `sql/analysis/70_language_publisher_rankings.sql` inside the Postgres container.

        .EXAMPLE
        PS> .\scripts\Invoke-Task03Run.ps1
        Runs all Task 03 SQL scripts in numeric order.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Position = 0, ValueFromPipeline, ValueFromPipelineByPropertyName)]
        [ValidateNotNullOrEmpty()]
        [string[]]$Script = @('all')
    )

    begin {
        $scriptMap = @{
            '60' = '60_top_books_per_author.sql'
            'authors' = '60_top_books_per_author.sql'
            '70' = '70_language_publisher_rankings.sql'
            'publishers' = '70_language_publisher_rankings.sql'
            'language' = '70_language_publisher_rankings.sql'
            '80' = '80_publication_year_rolling_stats.sql'
            'rolling' = '80_publication_year_rolling_stats.sql'
            'years' = '80_publication_year_rolling_stats.sql'
        }

        $composeFiles = '-f docker-compose.python.yml -f docker-compose.postgresql.yml'
        $baseCommand = "docker compose $composeFiles exec -e PAGER=cat postgres psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads -f /app/sql/analysis/{0}"

        $resolvedScripts = New-Object System.Collections.Generic.List[string]
    }

    process {
        foreach ($item in $Script) {
            if ($item -eq 'all') {
                $resolvedScripts.Add('60_top_books_per_author.sql')
                $resolvedScripts.Add('70_language_publisher_rankings.sql')
                $resolvedScripts.Add('80_publication_year_rolling_stats.sql')
                continue
            }

            if ($scriptMap.ContainsKey($item.ToLower())) {
                $resolvedScripts.Add($scriptMap[$item.ToLower()])
            }
            else {
                throw "Unknown script identifier '$item'. Use 60/70/80, authors/publishers/rolling, or 'all'."
            }
        }
    }

    end {
        if ($resolvedScripts.Count -eq 0) {
            throw 'No scripts resolved. Specify at least one script identifier.'
        }

        foreach ($sqlFile in $resolvedScripts) {
            Write-Host "Running Task 03 SQL: $sqlFile" -ForegroundColor Cyan
            $command = [string]::Format($baseCommand, $sqlFile)
            $process = Start-Process -FilePath 'powershell.exe' -ArgumentList "-NoLogo", "-NoProfile", "-Command", $command -NoNewWindow -PassThru -Wait
            if ($process.ExitCode -ne 0) {
                throw "Command failed for $sqlFile with exit code $($process.ExitCode)."
            }
        }

        Write-Host 'All requested Task 03 scripts completed successfully.' -ForegroundColor Green
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    Invoke-Task03Run @PSBoundParameters
}
