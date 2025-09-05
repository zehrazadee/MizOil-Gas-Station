# Escape sequence
# (\n, \t, \a, \b, \\, \")
#Concatenation - kankatanasiya deyilir, stringlərin toplanması

#decimal --- 
# digit ---  bu 3 - ü arasındakı fərq
#numeric --- 


#Homework
#Task 1
text = "Hello programmers"
new_text= text.replace('p', 'P')
print(new_text)

#Task 2 
s = 'qwertyuiqwopzercdscgnvxbhgmjlma'
görülen = []
təkrarlanan = []

for herf in s:
    if herf in görülen and herf not in təkrarlanan:
        print(herf, end=' ')
        təkrarlanan.append(herf)
    else:
        görülen.append(herf)


#Task 3
s = ' Hello World '
s = s.strip()
print(s)

#Task 4
course = 'Our course is best in the World, STEP IT ACADEMY Azerbaijan'
course = course.lower()
print(course)

#Task 5
website = 'http://www.google.com'

if website.startswith('www'):
    print("Website 'www' ilə başlayır.")
else:
    print("Website 'www' ilə başlamır.")

if website.endswith('com'):
    print("Website 'com' ilə bitir.")
else:
    print("Website 'com' ilə bitmir.")

