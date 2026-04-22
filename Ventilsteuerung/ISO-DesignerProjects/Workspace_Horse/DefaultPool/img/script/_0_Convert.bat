::Script

@echo off & setlocal

magick -version


cls
cd ..\img_original

for %%f in (*.gif) do (
    magick identify %%f
    echo.
    echo Processing %%f ...
    echo 1. Extract frames from GIF
    mkdir ..\img_frames\%%~nf 2>nul
    magick %%f -coalesce -define png:exclude-chunks=date,time ..\img_frames\%%~nf\frame_%%02d.png
    echo    Frames extracted to ..\img_frames\%%~nf\
    echo.
    echo 2. crop frames by 2px
    mkdir ..\img_cropped\%%~nf 2>nul
    for %%g in (..\img_frames\%%~nf\*.png) do (
        magick %%g -shave 2x2 -define png:exclude-chunks=date,time ..\img_cropped\%%~nf\%%~nxg
    )
    echo    Cropped frames in ..\img_cropped\%%~nf\
    echo.
    echo 3. resize cropped frames to 64x64 for SKM
    mkdir ..\img_resized_SKM\%%~nf 2>nul
    for %%g in (..\img_cropped\%%~nf\*.png) do (
        magick %%g -resize 64x64 -define png:exclude-chunks=date,time ..\img_resized_SKM\%%~nf\%%~nxg
    )
    echo    Resized frames in ..\img_resized_SKM\%%~nf\
    echo.
    echo 4. make monochrome PNG for SKM
    mkdir ..\img_monochrome_SKM\%%~nf 2>nul
    for %%g in (..\img_resized_SKM\%%~nf\*.png) do (
        magick %%g -monochrome -define png:exclude-chunks=date,time ..\img_monochrome_SKM\%%~nf\%%~nxg
    )
    echo    Monochrome frames in ..\img_monochrome_SKM\%%~nf\
    echo.
    echo 5. make BMP for SKM
    mkdir ..\img_SKM\%%~nf 2>nul
    for %%g in (..\img_monochrome_SKM\%%~nf\*.png) do (
        magick %%g BMP3:..\img_SKM\%%~nf\%%~ng.bmp
    )
    echo    BMP frames in ..\img_SKM\%%~nf\
    echo.
    echo 6. make monochrome PNG for DM (full size)
    mkdir ..\img_monochrome_DM\%%~nf 2>nul
    for %%g in (..\img_cropped\%%~nf\*.png) do (
        magick %%g -monochrome -define png:exclude-chunks=date,time ..\img_monochrome_DM\%%~nf\%%~nxg
    )
    echo    Monochrome DM frames in ..\img_monochrome_DM\%%~nf\
    echo.
    echo 7. make BMP for DM
    mkdir ..\img_DM\%%~nf 2>nul
    for %%g in (..\img_monochrome_DM\%%~nf\*.png) do (
        magick %%g BMP3:..\img_DM\%%~nf\%%~ng.bmp
    )
    echo    BMP DM frames in ..\img_DM\%%~nf\
    echo.
    echo DONE *************************************
    echo *
    echo *
)



pause