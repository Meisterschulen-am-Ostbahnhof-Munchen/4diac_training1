@echo off & setlocal EnableDelayedExpansion

magick -version

cls
cd ..\img_original

for %%f in (*.gif) do (
    magick identify "%%f"
    echo.
    echo Processing "%%f" ...
    
    set "fname=%%~nf"
    
    echo 1. Extract frames from GIF
    if not exist "..\img_frames\!fname!" mkdir "..\img_frames\!fname!"
    magick "%%f" -coalesce -define png:exclude-chunks=date,time "..\img_frames\!fname!\frame_%%02d.png"
    echo    Frames extracted to ..\img_frames\!fname!\
    echo.
    
    echo 2. Convert frames to 8-bit BMP with Web-Safe palette (216 colors)
    if not exist "..\img_DM_256\!fname!" mkdir "..\img_DM_256\!fname!"
    for %%g in (..\img_frames\!fname!\*.png) do (
        magick "%%g" -remap netscape: -type Palette BMP3:"..\img_DM_256\!fname!\%%~ng.bmp"
    )
    echo    Web-Safe BMP frames in ..\img_DM_256\!fname!\
    echo.

    echo 3. Calculate common background from all frames (Median)
    magick ..\img_DM_256\!fname!\frame_*.bmp -evaluate-sequence Median -remap netscape: -type Palette BMP3:"..\img_DM_256\!fname!\frame_BG.bmp"
    echo    frame_BG.bmp created in ..\img_DM_256\!fname!\
    echo.

    echo 4. Replace background pixels with pink (#FF00FF) for RLE compression
    for %%g in (..\img_DM_256\!fname!\frame_*.bmp) do (
        if /I not "%%~nxg"=="frame_BG.bmp" (
            magick "%%g" "..\img_DM_256\!fname!\frame_BG.bmp" -compose Difference -composite -threshold 0 "..\img_DM_256\!fname!\tmp_mask.png"
            magick "%%g" ( "..\img_DM_256\!fname!\tmp_mask.png" -alpha off ) -compose CopyOpacity -composite -background "#FF00FF" -alpha background -alpha remove -remap netscape: -type Palette BMP3:"%%g"
            del "..\img_DM_256\!fname!\tmp_mask.png"
        )
    )
    echo    Background pixels replaced with pink in all frames
    echo.

    echo DONE *************************************
    echo *
    echo *
)

pause
