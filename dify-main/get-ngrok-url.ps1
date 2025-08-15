#!/usr/bin/env powershell

Write-Host "Checking Ngrok tunnel status..."

for ($i = 1; $i -le 10; $i++) {
    try {
        Write-Host "Attempt $i/10..."
        $response = Invoke-WebRequest -Uri "http://localhost:4040/api/tunnels" -UseBasicParsing -TimeoutSec 5
        $data = $response.Content | ConvertFrom-Json
        
        if ($data.tunnels.Count -gt 0) {
            Write-Host "✅ Found tunnel!"
            $tunnel = $data.tunnels[0]
            Write-Host "Public URL: $($tunnel.public_url)"
            Write-Host "Protocol: $($tunnel.proto)"
            Write-Host "Local URL: $($tunnel.config.addr)"
            break
        } else {
            Write-Host "No tunnels found, waiting..."
        }
    }
    catch {
        Write-Host "Connection failed, retrying in 2 seconds..."
    }
    
    Start-Sleep 2
}

Write-Host "Done."
