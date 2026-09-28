from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
original=s

def sub_once(pattern,repl,label,flags=0):
    global s
    s2,n=re.subn(pattern,repl,s,count=1,flags=flags)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    s=s2

# Supabase client library, pinned.
sub_once(r'</div>\n<script>\n\(\(\)=>\{', '</div>\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.57.4/dist/umd/supabase.min.js"></script>\n<script>\n(()=>{', 'supabase script include')

# Employee real login form.
sub_once(
    r'<label class="field-label" for="employeeUser">Usuario</label><input id="employeeUser" class="control" autocomplete="username" value="empleado">\n    <label class="field-label" for="employeePass">Contraseña</label><input id="employeePass" class="control" type="password" autocomplete="current-password" value="empleado123">\n    <button id="employeeLoginBtn" class="btn btn-teal btn-full" type="button" style="margin-top:16px">Entrar</button>\n    <div class="demo-credentials">Demo: usuario <strong>empleado</strong> · contraseña <strong>empleado123</strong></div>',
    '<label class="field-label" for="employeeUser">Correo</label><input id="employeeUser" class="control" type="email" autocomplete="username" value="adrianstenerife@gmail.com">\n    <label class="field-label" for="employeePass">Contraseña</label><input id="employeePass" class="control" type="password" autocomplete="current-password" placeholder="Tu contraseña">\n    <button id="employeeLoginBtn" class="btn btn-teal btn-full" type="button" style="margin-top:16px">Entrar</button>\n    <button id="employeeSignupBtn" class="btn btn-secondary btn-full" type="button" style="margin-top:9px">Activar acceso por primera vez</button>\n    <div class="demo-credentials">Acceso autorizado para el empleado piloto. La primera vez elige una contraseña de al menos 6 caracteres y confirma el correo recibido.</div>',
    'employee login form')

# Manager real login form.
sub_once(
    r'<label class="field-label" for="managerUser">Usuario</label><input id="managerUser" class="control" autocomplete="username" value="empresa">\n    <label class="field-label" for="managerPass">Contraseña</label><input id="managerPass" class="control" type="password" autocomplete="current-password" value="empresa123">\n    <button id="managerLoginBtn" class="btn btn-primary btn-full" type="button" style="margin-top:16px">Entrar</button>\n    <div class="demo-credentials">Demo: usuario <strong>empresa</strong> · contraseña <strong>empresa123</strong></div>',
    '<label class="field-label" for="managerUser">Correo</label><input id="managerUser" class="control" type="email" autocomplete="username" value="1982mag.lil.aar@gmail.com">\n    <label class="field-label" for="managerPass">Contraseña</label><input id="managerPass" class="control" type="password" autocomplete="current-password" placeholder="Tu contraseña">\n    <button id="managerLoginBtn" class="btn btn-primary btn-full" type="button" style="margin-top:16px">Entrar</button>\n    <button id="managerSignupBtn" class="btn btn-secondary btn-full" type="button" style="margin-top:9px">Activar acceso por primera vez</button>\n    <div class="demo-credentials">Acceso autorizado para el responsable piloto. La primera vez elige una contraseña de al menos 6 caracteres y confirma el correo recibido.</div>',
    'manager login form')

# Supabase config and runtime vars.
sub_once(
    r"const credentials=\{employee:\{user:'empleado',pass:'empleado123'\},manager:\{user:'empresa',pass:'empresa123'\}\};",
    "const SUPABASE_URL='https://qmnqosftyinbzsypuyqa.supabase.co';\nconst SUPABASE_KEY='sb_publishable_KkxBCTZTf7XPZqmwj5tAYw_LDozNheK';\nconst supabaseClient=window.supabase.createClient(SUPABASE_URL,SUPABASE_KEY,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});\nconst credentials={employee:{user:'adrianstenerife@gmail.com'},manager:{user:'1982mag.lil.aar@gmail.com'}};",
    'supabase config')

sub_once(
    r"let state=load\(\);let currentLesson=0;let activeRole=null;",
    "let state=load();let currentLesson=0;let activeRole=null;let currentProfile=null;let questionsChannel=null;",
    'runtime vars')

# Replace login implementation with real Supabase Auth + profile authorization.
sub_once(
    r"function login\(role\)\{const isEmp=role==='employee';const user=\$\(isEmp\?'employeeUser':'managerUser'\)\.value\.trim\(\);const pass=\$\(isEmp\?'employeePass':'managerPass'\)\.value;const fb=\$\(isEmp\?'employeeLoginFeedback':'managerLoginFeedback'\);if\(user===credentials\[role\]\.user&&pass===credentials\[role\]\.pass\)\{fb\.textContent='';activeRole=role;show\(isEmp\?'screen-employee':'screen-manager'\)\}else\{fb\.textContent='Usuario o contraseña incorrectos\.';fb\.className='feedback error'\}\}",
    "async function loadProfile(userId){const {data,error}=await supabaseClient.from('profiles').select('user_id,company_id,full_name,role').eq('user_id',userId).single();if(error)return null;return data}\nfunction fmtRemoteDate(ts){if(!ts)return '';try{return new Date(ts).toLocaleString('es-ES',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'})}catch(e){return ts}}\nasync function loadRemoteQuestions(){if(!currentProfile)return;const {data,error}=await supabaseClient.from('questions').select('*').order('created_at',{ascending:true});if(error){console.error('questions load',error);return}state.questions=(data||[]).map(r=>{const idx=Number(r.module_key);return{id:r.id,employeeId:r.employee_id,moduleIndex:Number.isFinite(idx)?idx:null,moduleTitle:r.module_title||'Formación',area:Number.isFinite(idx)&&modules[idx]?modules[idx].area:'Comunicación',text:r.question_text,createdAt:fmtRemoteDate(r.created_at),updatedAt:fmtRemoteDate(r.updated_at),status:r.status,answer:r.answer_text||'',answeredAt:fmtRemoteDate(r.answered_at)}});if(currentProfile.role==='manager'){const {data:emps}=await supabaseClient.from('profiles').select('user_id,full_name,role').eq('role','employee').limit(1);if(emps&&emps[0]){state.employee.id=emps[0].user_id;state.employee.name=emps[0].full_name||state.employee.name}}else{state.employee.id=currentProfile.user_id;state.employee.name=currentProfile.full_name||state.employee.name}}\nfunction refreshRemoteUI(){if(document.querySelector('#screen-employee.active'))renderEmployee();if(document.querySelector('#screen-manager.active'))renderManager();if(document.querySelector('#screen-lesson.active'))openLesson(currentLesson)}\nfunction startQuestionsRealtime(){if(questionsChannel){supabaseClient.removeChannel(questionsChannel);questionsChannel=null}questionsChannel=supabaseClient.channel('questions-pilot').on('postgres_changes',{event:'*',schema:'public',table:'questions'},async()=>{await loadRemoteQuestions();refreshRemoteUI()}).subscribe()}\nasync function login(role){const isEmp=role==='employee',email=$(isEmp?'employeeUser':'managerUser').value.trim().toLowerCase(),pass=$(isEmp?'employeePass':'managerPass').value,fb=$(isEmp?'employeeLoginFeedback':'managerLoginFeedback');fb.textContent='';if(!email||!pass){fb.textContent='Introduce correo y contraseña.';fb.className='feedback error';return}const {data,error}=await supabaseClient.auth.signInWithPassword({email,password:pass});if(error){fb.textContent='No se pudo iniciar sesión. Revisa la contraseña o activa primero el acceso.';fb.className='feedback error';return}const profile=await loadProfile(data.user.id);if(!profile||profile.role!==role){await supabaseClient.auth.signOut();fb.textContent='Este correo no está autorizado para esta zona.';fb.className='feedback error';return}currentProfile=profile;activeRole=role;await loadRemoteQuestions();startQuestionsRealtime();show(isEmp?'screen-employee':'screen-manager')}\nasync function signup(role){const isEmp=role==='employee',email=$(isEmp?'employeeUser':'managerUser').value.trim().toLowerCase(),pass=$(isEmp?'employeePass':'managerPass').value,fb=$(isEmp?'employeeLoginFeedback':'managerLoginFeedback');fb.textContent='';if(email!==credentials[role].user){fb.textContent='Este correo no está autorizado para el piloto.';fb.className='feedback error';return}if(pass.length<6){fb.textContent='La contraseña debe tener al menos 6 caracteres.';fb.className='feedback error';return}const {data,error}=await supabaseClient.auth.signUp({email,password:pass,options:{emailRedirectTo:location.origin+location.pathname}});if(error){fb.textContent=error.message.includes('already')?'La cuenta ya existe. Pulsa Entrar con tu contraseña.':'No se pudo activar el acceso: '+error.message;fb.className='feedback error';return}if(data.session){const profile=await loadProfile(data.user.id);if(profile){currentProfile=profile;activeRole=role;await loadRemoteQuestions();startQuestionsRealtime();show(isEmp?'screen-employee':'screen-manager');return}}fb.textContent='Te hemos enviado un correo de confirmación. Ábrelo y después vuelve a entrar.';fb.className='feedback success'}\nasync function restoreSession(){const {data:{session}}=await supabaseClient.auth.getSession();if(!session)return;const profile=await loadProfile(session.user.id);if(!profile)return;currentProfile=profile;activeRole=profile.role;await loadRemoteQuestions();startQuestionsRealtime();show(profile.role==='employee'?'screen-employee':'screen-manager')}",
    'real login logic')

# Add remote answered questions to employee notifications.
sub_once(
    r"const alerts=\$\('employeeNotifications'\);alerts\.replaceChildren\(\);const visible=state\.alerts\.slice\(\)\.reverse\(\)\.slice\(0,6\);if\(!visible\.length\)\{const d=document\.createElement\('div'\);d\.className='card muted';d\.textContent='No hay avisos del responsable\.';alerts\.append\(d\)\}visible\.forEach\(a=>\{",
    "const alerts=$('employeeNotifications');alerts.replaceChildren();const answeredQuestions=state.questions.filter(q=>q.status==='resolved'&&q.answer).slice().reverse().slice(0,4);const visible=state.alerts.slice().reverse().slice(0,6);if(!visible.length&&!answeredQuestions.length){const d=document.createElement('div');d.className='card muted';d.textContent='No hay avisos del responsable.';alerts.append(d)}answeredQuestions.forEach(q=>{const d=document.createElement('div');d.className='notification good';const sm=document.createElement('small');sm.textContent='Respuesta del responsable · '+(q.answeredAt||'');const b=document.createElement('div');b.textContent=q.answer;d.append(sm,b);alerts.append(d)});visible.forEach(a=>{",
    'employee remote answers')

# Replace manager response action with Supabase update.
sub_once(
    re.escape("btn.addEventListener('click',()=>{const answer=ta.value.trim();if(!answer){ta.focus();return}q.answer=answer;q.status='resolved';q.answeredAt=stamp();q.updatedAt=q.answeredAt;const m=modules[q.moduleIndex];addAlert(m?m.area:q.area||'Comunicación','Tu responsable respondió a tu duda: '+answer,'Respuesta del responsable');save();renderManager()});"),
    "btn.addEventListener('click',async()=>{const answer=ta.value.trim();if(!answer){ta.focus();return}if(!currentProfile||currentProfile.role!=='manager'){return}btn.disabled=true;const now=new Date().toISOString();const {error}=await supabaseClient.from('questions').update({answer_text:answer,status:'resolved',answered_by:currentProfile.user_id,answered_at:now,updated_at:now}).eq('id',q.id);btn.disabled=false;if(error){alert('No se pudo guardar la respuesta: '+error.message);return}await loadRemoteQuestions();renderManager()});",
    'manager remote answer')

# Replace lesson doubt save with remote insert.
sub_once(
    re.escape("$('lessonPracticed').addEventListener('change',e=>{state.employee.activities[currentLesson]={...record(currentLesson),practiced:e.target.checked,updatedAt:stamp()};save();});$('saveLessonNote').addEventListener('click',()=>{const text=$('lessonNote').value.trim();if(!text){$('lessonNoteFeedback').textContent='Escribe la duda antes de enviarla.';$('lessonNoteFeedback').className='feedback error';return}const now=stamp(),m=modules[currentLesson];state.employee.activities[currentLesson]={...record(currentLesson),note:text,updatedAt:now};let q=state.questions.slice().reverse().find(q=>q.moduleIndex===currentLesson&&q.status!=='resolved');if(q){q.text=text;q.updatedAt=now}else{state.questions.push({id:Date.now()+Math.random(),employeeId:state.employee.id,moduleIndex:currentLesson,moduleTitle:m.title,area:m.area,text,createdAt:now,updatedAt:now,status:'pending',answer:'',answeredAt:null})}save();openLesson(currentLesson);$('lessonNoteFeedback').textContent='Duda enviada al responsable.';$('lessonNoteFeedback').className='feedback success'});"),
    "$('lessonPracticed').addEventListener('change',e=>{state.employee.activities[currentLesson]={...record(currentLesson),practiced:e.target.checked,updatedAt:stamp()};save();});$('saveLessonNote').addEventListener('click',async()=>{const text=$('lessonNote').value.trim(),fb=$('lessonNoteFeedback');if(!text){fb.textContent='Escribe la duda antes de enviarla.';fb.className='feedback error';return}if(!currentProfile||currentProfile.role!=='employee'){fb.textContent='Debes entrar con el acceso real del empleado.';fb.className='feedback error';return}if(state.questions.some(q=>q.moduleIndex===currentLesson&&q.status!=='resolved')){fb.textContent='Ya tienes una duda pendiente en este módulo.';fb.className='feedback error';return}const m=modules[currentLesson],now=stamp();state.employee.activities[currentLesson]={...record(currentLesson),note:text,updatedAt:now};save();const {error}=await supabaseClient.from('questions').insert({company_id:currentProfile.company_id,employee_id:currentProfile.user_id,module_key:String(currentLesson),module_title:m.title,question_text:text,status:'pending'});if(error){fb.textContent='No se pudo enviar la duda: '+error.message;fb.className='feedback error';return}await loadRemoteQuestions();openLesson(currentLesson);fb.textContent='Duda enviada al responsable.';fb.className='feedback success'});",
    'employee remote question')

# Wire activation buttons.
sub_once(
    re.escape("$('openEmployeeLogin').addEventListener('click',()=>show('screen-login-employee'));$('openManagerLogin').addEventListener('click',()=>show('screen-login-manager'));$('employeeLoginBtn').addEventListener('click',()=>login('employee'));$('managerLoginBtn').addEventListener('click',()=>login('manager'));"),
    "$('openEmployeeLogin').addEventListener('click',()=>show('screen-login-employee'));$('openManagerLogin').addEventListener('click',()=>show('screen-login-manager'));$('employeeLoginBtn').addEventListener('click',()=>login('employee'));$('managerLoginBtn').addEventListener('click',()=>login('manager'));$('employeeSignupBtn').addEventListener('click',()=>signup('employee'));$('managerSignupBtn').addEventListener('click',()=>signup('manager'));",
    'auth button wiring')

# Restore session on return from confirmation link.
sub_once(r"show\('screen-home'\);\n\}\)\(\);", "show('screen-home');restoreSession();\n})();", 'session restore')

if s==original:
    raise SystemExit('No changes produced')
p.write_text(s,encoding='utf-8')
print('Patched index.html',len(original),'->',len(s))
