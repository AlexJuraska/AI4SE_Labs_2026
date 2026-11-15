## Task 1 - Cloning a repository

The agent was given the following prompt

```
Clone the following repository 

https://github.com/Neltharion59/AI4SE_Playground

into the folder Week_06_Implementation\Assignments
```

The agent responded by running the following command

```
$destination = Join-Path (Get-Location) 'Week_06_Implementation\Assignments\AI4SE_Playground'; if (Test-Path -LiteralPath $destination) { Write-Error "Destination already exists: $destination"; exit 1 }; git clone 'https://github.com/Neltharion59/AI4SE_Playground' $destination; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; git -C $destination rev-parse --show-toplevel; git -C $destination branch --show-current
```

With it, the repository was cloned correctly. The agent could do this because it has a terminal tool, which lets it run commands. It used git clone to download the repository, then two more git commands to check that the clone worked.