::Script

@echo off & setlocal

magick -version


cls
cd ..\img_original

for %%f in (*.png) do (
    magick identify %%f
    magick %%f -crop   196x196+2+2 ..\img_cropped\%%f
)



pause