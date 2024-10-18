#PS
# 获取当前目录
$RootPath = Get-Location

# 获取脚本自身文件名
$ScriptName = $MyInvocation.MyCommand.Name

# 遍历目录及其子目录中的所有文件
Get-ChildItem -Path $RootPath -Recurse -File | ForEach-Object {
    $File = $_

    # 获取文件的完整路径
    $FilePath = $File.FullName

    # 跳过脚本自身
    if ($File.Name -eq $ScriptName) {
        Write-Output "Skipped '$FilePath' - this is the rename script."
        return
    }

    # 使用 \\?\ 前缀以支持超长路径
    $LongFilePath = "\\?\$FilePath"

    # 获取文件的修改时间，并转换为 yyyymmdd 格式
    $ModifiedDate = $File.LastWriteTime.ToString("yyyyMMdd")

    # 获取文件的原始名称
    $OriginalFileName = $File.Name

    # 检查文件名是否已经包含 yyyymmdd 日期前缀
    if ($OriginalFileName -notmatch '^\d{8}_') {
        # 构建新的文件名
        $NewFileName = "${ModifiedDate}_$OriginalFileName"

        # 获取新文件路径，并使用 \\?\ 前缀处理长路径
        $NewFilePath = Join-Path -Path $File.DirectoryName -ChildPath $NewFileName
        $LongNewFilePath = "\\?\$NewFilePath"

        # 检查文件是否存在（启用OneDrive文件随取后，有时候会提示文件不存在）
        if (Test-Path -Path $LongFilePath) {
            # 使用 Move-Item 进行重命名 获取更好兼容性的啦
            Move-Item -Path $LongFilePath -Destination $LongNewFilePath

            Write-Output "Renamed '$FilePath' to '$NewFilePath'"
        } else {
            Write-Output "File not found: '$FilePath'"
        }
    } else {
        Write-Output "Skipped '$OriginalFileName' - already has a date prefix."
    }
}
