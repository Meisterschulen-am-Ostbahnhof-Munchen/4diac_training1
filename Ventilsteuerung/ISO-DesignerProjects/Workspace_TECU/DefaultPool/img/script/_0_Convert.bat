::Script

@echo off & setlocal

magick -version


cls
cd ..\img_original

for %%f in (*.png) do (
    magick identify %%f
    echo 1. crop Bitmap by 2px 
    magick %%f -shave   2x2 ..\img_cropped\%%f -define png:exclude-chunks=date
    magick identify ..\img_cropped\%%f
    echo 2. resize to 64x64
    magick ..\img_cropped\%%f  -resize  64x64       ..\img_resized\%%f  -define png:exclude-chunks=date
    magick identify ..\img_resized\%%f
    echo 3. make monochrome PNG
    magick ..\img_cropped\%%f  -monochrome       ..\img_monochrome\%%f -define png:exclude-chunks=date
    magick identify ..\img_monochrome\%%f
    echo 4. make BMP
    magick ..\img_monochrome\%%f    ..\img\%%~nf.bmp
    magick identify ..\img\%%~nf.bmp
    echo DONE *************************************
    echo *
    echo *
)



pause