from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s
s=s.replace('value="adrianstenerife@gmail.com"','value="1982mag.lil.aar@gmail.com"',1)
s=s.replace('Acceso autorizado para el empleado piloto. La primera vez elige una contraseña de al menos 6 caracteres y confirma el correo recibido.','Modo piloto: usa temporalmente la misma cuenta del responsable para probar la sincronización entre dos dispositivos. No pulses “Activar acceso” en esta pantalla.',1)
s=s.replace("const credentials={employee:{user:'adrianstenerife@gmail.com'},manager:{user:'1982mag.lil.aar@gmail.com'}};","const credentials={employee:{user:'1982mag.lil.aar@gmail.com'},manager:{user:'1982mag.lil.aar@gmail.com'}};",1)
old="if(!profile||profile.role!==role){await supabaseClient.auth.signOut();fb.textContent='Este correo no está autorizado para esta zona.';fb.className='feedback error';return}currentProfile=profile;activeRole=role;"
new="const pilotEmployeeAccess=(role==='employee'&&profile&&profile.role==='manager'&&email===credentials.manager.user);if(!profile||(profile.role!==role&&!pilotEmployeeAccess)){await supabaseClient.auth.signOut();fb.textContent='Este correo no está autorizado para esta zona.';fb.className='feedback error';return}currentProfile={...profile,role:pilotEmployeeAccess?'employee':profile.role};activeRole=role;"
if old not in s:
    raise SystemExit('login guard not found')
s=s.replace(old,new,1)
old2="if(!currentProfile||currentProfile.role!=='employee'){fb.textContent='Debes entrar con el acceso real del empleado.';fb.className='feedback error';return}"
new2="if(!currentProfile||currentProfile.role!=='employee'){fb.textContent='Debes entrar desde la zona de empleado.';fb.className='feedback error';return}"
s=s.replace(old2,new2,1)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('patched')
