# Define the path to the input file
$inputFilePath = "test.json"

# Define the path to the output file
$outputFilePath = "test.b64"

# Read the content of the input file
$fileContent = Get-Content -Path $inputFilePath -Raw

# Convert the content to a byte array using UTF8 encoding
$byteArray = [System.Text.Encoding]::UTF8.GetBytes($fileContent)

# Convert the byte array to a Base64 string
$base64String = [Convert]::ToBase64String($byteArray)

# Write the Base64 string to the output file
Set-Content -Path $outputFilePath -Value $base64String
