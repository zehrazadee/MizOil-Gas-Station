#Bu program tarix və saat ilə işləməyi göstərir

import datetime
today = datetime.date.today()  #Cari tarixi tapır
print("Bugünkü tarix:", today)

now = datetime.datetime.now() #Tarixi + saatı verir
print("Tam vaxt:", now)

time = now.time()  #Yalnız saatı çıxarır
print("cari saat:", time)
