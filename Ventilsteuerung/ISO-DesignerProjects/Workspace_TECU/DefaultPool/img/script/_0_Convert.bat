::Script

@echo off & setlocal

magick -version


cls
cd ..\img_original

for %%f in (*.png) do (
    magick identify %%f
    echo crop Bitmap by 2px 
    magick %%f -shave   2x2 ..\img_cropped\%%f
    magick identify ..\img_cropped\%%f
)



pause