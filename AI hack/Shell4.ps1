#Shell4.ps1
#Usage:PS C:\Scripts> .\Shell4.ps1 -media "video-file" -dataset "data-dir"
#py program6.py E:\project\openCV\accident.mp4 E:\project\openCV\data3\
#py access_test.py E:\project\openCV\data3

param($media,$dataset)

[string]$command1_prog = "py E:\project\openCV\image_process.py "
[string]$command2_prog = "py E:\project\test\output\final.py "

iex $media

[string]$command1 = ($command1_prog + $media+ " " + $dataset + "\")
iex $command1

[string]$command2 = ($command2_prog + $dataset)
iex $command2