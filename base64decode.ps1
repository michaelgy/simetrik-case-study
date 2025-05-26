# Define the path to the Base64-encoded file
$base64FilePath = "test.b64"

# Define the path to the decoded output file
$decodedFilePath = "test.json"

# Read the Base64 string from the file
$base64String = Get-Content -Path $base64FilePath -Raw

# Convert the Base64 string back to a byte array
$byteArray = [Convert]::FromBase64String($base64String)

# Convert the byte array back to a string using UTF8 encoding
$originalContent = [System.Text.Encoding]::UTF8.GetString($byteArray)

# Write the original content to the decoded file
Set-Content -Path $decodedFilePath -Value $originalContent