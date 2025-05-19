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
REM
    echo 2. resize to 64x64 for SKM
    magick ..\img_cropped\%%f -resize 64x64 -define png:exclude-chunks=date,time ..\img_resized_SKM\%%f  
    magick identify ..\img_resized_SKM\%%f
    echo 2. do not resize for DM
    echo 2. resize to 98x98 for DM_2
    magick ..\img_cropped\%%f -resize 98x98 -define png:exclude-chunks=date,time ..\img_resized_DM_2\%%f  
    magick identify ..\img_resized_DM_2\%%f
REM
    echo 3. make monochrome PNG for SKM
    magick ..\img_resized_SKM\%%f -monochrome -define png:exclude-chunks=date,time ..\img_monochrome_SKM\%%f 
    magick identify ..\img_monochrome_SKM\%%f
    echo 3. make monochrome PNG for DM
    magick ..\img_cropped\%%f -monochrome -define png:exclude-chunks=date,time ..\img_monochrome_DM\%%f 
    magick identify ..\img_monochrome_DM\%%f
    echo 3. make monochrome PNG for DM_2
    magick ..\img_resized_DM_2\%%f -monochrome -define png:exclude-chunks=date,time ..\img_monochrome_DM_2\%%f 
    magick identify ..\img_monochrome_DM_2\%%f
REM
    echo 4. make BMP for SKM
    magick ..\img_monochrome_SKM\%%f BMP3:..\img_SKM\%%~nf.bmp
    magick identify ..\img_SKM\%%~nf.bmp
    echo 4. make BMP for DM
    magick ..\img_monochrome_DM\%%f BMP3:..\img_DM\%%~nf.bmp
    magick identify ..\img_DM\%%~nf.bmp
    echo 4. make BMP for DM
    magick ..\img_monochrome_DM_2\%%f BMP3:..\img_DM_2\%%~nf.bmp
    magick identify ..\img_DM_2\%%~nf.bmp
REM
    echo DONE *************************************
    echo *
    echo *
)



pause