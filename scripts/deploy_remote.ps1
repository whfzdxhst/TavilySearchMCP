param(
    [Parameter(Mandatory = $true)]
    [string]$HostName,
    [string]$User = "ubuntu",
    [string]$RemoteDir = "tavily-search-mcp",
    [string]$IdentityFile = ""
)

$ErrorActionPreference = "Stop"

$archive = Join-Path $PWD "tavily-search-mcp.tar.gz"
if (Test-Path $archive) {
    Remove-Item -LiteralPath $archive -Force
}

tar `
    --exclude=".git" `
    --exclude=".conda" `
    --exclude=".conda-pkgs" `
    --exclude=".env" `
    --exclude="tavily-search-mcp.tar.gz" `
    -czf $archive .

$sshTarget = "$User@$HostName"
$sshArgs = @()
$scpArgs = @()
if ($IdentityFile -ne "") {
    $sshArgs += @("-i", $IdentityFile, "-o", "IdentitiesOnly=yes")
    $scpArgs += @("-i", $IdentityFile, "-o", "IdentitiesOnly=yes")
}

ssh @sshArgs $sshTarget "mkdir -p '$RemoteDir'"
scp @scpArgs $archive "$sshTarget`:/tmp/tavily-search-mcp.tar.gz"
ssh @sshArgs $sshTarget "tar -xzf /tmp/tavily-search-mcp.tar.gz -C '$RemoteDir' && cd '$RemoteDir' && chmod +x scripts/bootstrap_remote.sh && MCP_SERVER_HOST=0.0.0.0 MCP_SERVER_PORT=21029 scripts/bootstrap_remote.sh"

Remove-Item -LiteralPath $archive -Force
