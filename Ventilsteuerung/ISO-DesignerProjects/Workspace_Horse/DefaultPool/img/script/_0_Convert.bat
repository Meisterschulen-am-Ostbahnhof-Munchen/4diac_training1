::Script

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
    
    echo 2. resize frames to 64x64 for SKM
    if not exist "..\img_resized_SKM\!fname!" mkdir "..\img_resized_SKM\!fname!"
    for %%g in (..\img_frames\!fname!\*.png) do (
        magick "%%g" -resize 64x64 -define png:exclude-chunks=date,time "..\img_resized_SKM\!fname!\%%~nxg"
    )
    echo    Resized frames in ..\img_resized_SKM\!fname!\
    echo.

    echo 3. make monochrome PNG for SKM
    if not exist "..\img_monochrome_SKM\!fname!" mkdir "..\img_monochrome_SKM\!fname!"
    for %%g in (..\img_resized_SKM\!fname!\*.png) do (
        magick "%%g" -monochrome -define png:exclude-chunks=date,time "..\img_monochrome_SKM\!fname!\%%~nxg"
    )
    echo    Monochrome frames in ..\img_monochrome_SKM\!fname!\
    echo.

    echo 4. make BMP for SKM
    if not exist "..\img_SKM\!fname!" mkdir "..\img_SKM\!fname!"
    for %%g in (..\img_monochrome_SKM\!fname!\*.png) do (
        magick "%%g" BMP3:"..\img_SKM\!fname!\%%~ng.bmp"
    )
    echo    BMP frames in ..\img_SKM\!fname!\
    echo.

    echo 5. make 256 color PNG for SKM
    if not exist "..\img_256_SKM\!fname!" mkdir "..\img_256_SKM\!fname!"
    for %%g in (..\img_resized_SKM\!fname!\*.png) do (
        magick "%%g" -colors 256 -dither None -define png:exclude-chunks=date,time "..\img_256_SKM\!fname!\%%~nxg"
    )
    echo    256 color frames in ..\img_256_SKM\!fname!\
    echo.

    echo 6. make BMP for SKM 256 colors
    if not exist "..\img_SKM_256\!fname!" mkdir "..\img_SKM_256\!fname!"
    for %%g in (..\img_256_SKM\!fname!\*.png) do (
        magick "%%g" -type Palette -compress none BMP3:"..\img_SKM_256\!fname!\%%~ng.bmp"
    )
    echo    BMP 256 frames in ..\img_SKM_256\!fname!\
    echo.

    echo 7. make monochrome PNG for DM (full size)
    if not exist "..\img_monochrome_DM\!fname!" mkdir "..\img_monochrome_DM\!fname!"
    for %%g in (..\img_frames\!fname!\*.png) do (
        magick "%%g" -monochrome -define png:exclude-chunks=date,time "..\img_monochrome_DM\!fname!\%%~nxg"
    )
    echo    Monochrome DM frames in ..\img_monochrome_DM\!fname!\
    echo.

    echo 8. make BMP for DM
    if not exist "..\img_DM\!fname!" mkdir "..\img_DM\!fname!"
    for %%g in (..\img_monochrome_DM\!fname!\*.png) do (
        magick "%%g" BMP3:"..\img_DM\!fname!\%%~ng.bmp"
    )
    echo    BMP DM frames in ..\img_DM\!fname!\
    echo.

    echo 9. make 256 color PNG for DM (full size)
    if not exist "..\img_256_DM\!fname!" mkdir "..\img_256_DM\!fname!"
    for %%g in (..\img_frames\!fname!\*.png) do (
        magick "%%g" -colors 256 -dither None -define png:exclude-chunks=date,time "..\img_256_DM\!fname!\%%~nxg"
    )
    echo    256 color DM frames in ..\img_256_DM\!fname!\
    echo.

    echo 10. make BMP for DM 256 colors
    if not exist "..\img_DM_256\!fname!" mkdir "..\img_DM_256\!fname!"
    for %%g in (..\img_256_DM\!fname!\*.png) do (
        magick "%%g" -type Palette -compress none BMP3:"..\img_DM_256\!fname!\%%~ng.bmp"
    )
    echo    BMP 256 DM frames in ..\img_DM_256\!fname!\
    echo.
    
    echo DONE *************************************
    echo *
    echo *
)

pause