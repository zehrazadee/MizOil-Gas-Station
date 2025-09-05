#Bu program fayl və qovluqlar ilə işləməyi göstərir

import os
print("Hazırki qovluq:", os.getcwd())
print("Bu qovluqdakı fayllar:", os.listdir())

#Əgər yoxdursa, yeni qovluq yaratmaq
if not os.path.exists("yeni_qovluq"):
    os.mkdir("yeni_qovluq")
    print("yeni_qovluq yaradıldı")