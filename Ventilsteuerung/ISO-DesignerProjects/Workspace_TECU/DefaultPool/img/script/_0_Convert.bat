::Script

::@echo off & setlocal

magick -version


cls
cd ..\img_original

for %%f in (*.png) do (
    echo %%f
    magick identify %%f
    ::magick %%f -crop   196x196+2+2 ..\img_cropped\%%f
    ::magick ..\img_cropped\%%f  -resize  64x64       ..\img_resized\%%f
    ::magick convert ..\img_resized\%%f  -threshold 85 -type bilevel BMP3:..\img\%%~nf.bmp
)


pause