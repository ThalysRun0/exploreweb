Get-Content "source_url.lst" | ForEach-Object {
    $url = $_
    python ./main.py "$url" -d 2 -w
}
