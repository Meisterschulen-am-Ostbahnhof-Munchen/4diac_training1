::Script

@echo off & setlocal

magick -version


cls
cd ..\img_original

for %%f in (*.png) do (
    magick identify %%f
    echo 1. crop Bitmap by 2px 
    magick %%f -shave 2x2 -define png:exclude-chunks=date,time ..\img_cropped\%%f 
    magick identify ..\img_cropped\%%f
    echo 2. resize to 64x64
    magick ..\img_cropped\%%f -resize 64x64 -define png:exclude-chunks=date,time ..\img_resized\%%f  
    magick identify ..\img_resized\%%f
    echo 3. make monochrome PNG
    magick ..\img_resized\%%f -monochrome -define png:exclude-chunks=date,time ..\img_monochrome\%%f 
    magick identify ..\img_monochrome\%%f
    echo 4. make BMP
    magick ..\img_monochrome\%%f BMP3:..\img\%%~nf.bmp
    magick identify ..\img\%%~nf.bmp
    echo DONE *************************************
    echo *
    echo *
)



pause