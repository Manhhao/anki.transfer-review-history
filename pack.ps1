$target = 'Transfer Review History.zip'
$rnTarget = 'Transfer Review History.ankiaddon'
$files = New-Object -TypeName 'System.Collections.ArrayList'

$files.Add('__init__.py')
$files.Add('config.json')
$files.Add('LICENSE')
$files.Add('README.md')

If (Test-Path -Path $target -PathType Leaf)
{
  Remove-Item -Path $target
}

Compress-Archive -Path $($files) -DestinationPath $target
Move-Item $target $rnTarget -Force
