from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s
repls=[
('value="adrianstenerife@gmail.com"','value="Luciaamaralcorrea@gmail.com"'),
("const credentials={employee:{user:'adrianstenerife@gmail.com'},manager:{user:'1982mag.lil.aar@gmail.com'}};","const credentials={employee:{user:'luciaamaralcorrea@gmail.com'},manager:{user:'1982mag.lil.aar@gmail.com'}};"),
('Acceso autorizado para el empleado piloto. La primera vez elige una contraseña de al menos 6 caracteres y confirma el correo recibido.','Acceso autorizado para Lucía. La primera vez elige una contraseña de al menos 6 caracteres.'),
('<h2 id="managerEmployeeName" style="margin-bottom:5px">Juan Pérez</h2>','<h2 id="managerEmployeeName" style="margin-bottom:5px">Lucía</h2>'),
("const blankState=()=>({employee:{id:'juan',name:'Juan Pérez',role:'Camarero sala',day:7,activities:{}},observations:[],evaluations:[],alerts:[],questions:[]});","const blankState=()=>({employee:{id:'lucia-pilot',name:'Lucía',role:'Camarero sala',day:7,activities:{}},observations:[],evaluations:[],alerts:[],questions:[]});"),
(".from('profiles').select('user_id,full_name,role').eq('role','employee').limit(1)",".from('profiles').select('user_id,full_name,role').eq('role','employee').eq('full_name','Lucía').limit(1)"),
("let state=load();let currentLesson=0;let activeRole=null;let currentProfile=null;let questionsChannel=null;","let state=load();state.employee.name='Lucía';state.employee.role='Camarero sala';let currentLesson=0;let activeRole=null;let currentProfile=null;let questionsChannel=null;")
]
for a,b in repls:
    if a in s:
        s=s.replace(a,b,1)
if s==orig:
    raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('patched Lucia identity')
