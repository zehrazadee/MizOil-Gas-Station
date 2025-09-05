#Bu program JSON ilə işləməyi göstərir

import json
student = {"name": "Ayan", "age": 16, "subject": ["Python", "Math"]}

#Python --> JSON
json_student = json.dumps(student)
print("JSON formatında:", json_student)

#JSON --> Python
python_student = json.loads(json_student)
print("Python formatında:", python_student)