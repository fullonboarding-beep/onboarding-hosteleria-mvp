from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
original = s

def replace_once(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, found {count}')
    s = s.replace(old, new, 1)

replace_once(
    ".timeline-item{border-left:3px solid #c6d5df;padding:8px 0 8px 12px}.timeline-item strong{display:block}.timeline-item small{color:var(--muted)}.nav{",
    ".timeline-item{border-left:3px solid #c6d5df;padding:8px 0 8px 12px}.timeline-item strong{display:block}.timeline-item small{color:var(--muted)}.question-card{border-left:4px solid #d39b25}.question-card.resolved{border-left-color:#57906a}.question-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}.question-answer{margin-top:10px;padding:10px 12px;border-radius:10px;background:#edf7f4}.question-status{font-size:.78rem;font-weight:800}.nav{",
    'question styles'
)

replace_once(
    '  <article class="card"><h3 style="margin-top:0">Mis dudas</h3><textarea id="lessonNote" class="control" rows="3" maxlength="300" placeholder="Anota una duda para consultarla con tu responsable"></textarea><button id="saveLessonNote" class="btn btn-secondary btn-full" type="button" style="margin-top:10px">Guardar nota</button><div id="lessonNoteFeedback" class="feedback"></div></article>',
    '  <article class="card"><h3 style="margin-top:0">Mis dudas</h3><textarea id="lessonNote" class="control" rows="3" maxlength="300" placeholder="Escribe una duda para tu responsable"></textarea><button id="saveLessonNote" class="btn btn-secondary btn-full" type="button" style="margin-top:10px">Enviar duda al responsable</button><div id="lessonNoteFeedback" class="feedback"></div><div id="lessonQuestionStatus"></div></article>',
    'employee question card'
)

replace_once(
    '  <div class="toolbar" style="margin-top:12px"><button id="newObservationBtn" class="btn btn-secondary" type="button">+ Observación</button><button id="newEvaluationBtn" class="btn btn-primary" type="button">Evaluar</button></div>\n  <h3>Evolución por criterio</h3><div id="managerAreas" class="card"></div>',
    '  <div class="toolbar" style="margin-top:12px"><button id="newObservationBtn" class="btn btn-secondary" type="button">+ Observación</button><button id="newEvaluationBtn" class="btn btn-primary" type="button">Evaluar</button></div>\n  <div class="section-head"><h3>Dudas del empleado</h3><span id="managerQuestionsCount" class="status">0 pendientes</span></div><div id="managerQuestions" class="stack"></div>\n  <h3>Evolución por criterio</h3><div id="managerAreas" class="card"></div>',
    'manager question section'
)

replace_once(
    "const blankState=()=>({employee:{id:'juan',name:'Juan Pérez',role:'Camarero sala',day:7,activities:{}},observations:[],evaluations:[],alerts:[]});",
    "const blankState=()=>({employee:{id:'juan',name:'Juan Pérez',role:'Camarero sala',day:7,activities:{}},observations:[],evaluations:[],alerts:[],questions:[]});",
    'blank state'
)

replace_once(
    "function load(){try{const x=JSON.parse(localStorage.getItem(KEY));if(x&&x.employee&&x.employee.activities&&Array.isArray(x.observations)&&Array.isArray(x.evaluations)&&Array.isArray(x.alerts))return x;}catch(e){}return blankState()}",
    "function load(){try{const x=JSON.parse(localStorage.getItem(KEY));if(x&&x.employee&&x.employee.activities&&Array.isArray(x.observations)&&Array.isArray(x.evaluations)&&Array.isArray(x.alerts)){if(!Array.isArray(x.questions))x.questions=[];Object.entries(x.employee.activities).forEach(([i,r])=>{if(r&&r.note&&!x.questions.some(q=>q.moduleIndex===Number(i)&&q.text===r.note)){x.questions.push({id:'legacy-'+i+'-'+Date.now(),employeeId:x.employee.id,moduleIndex:Number(i),moduleTitle:modules[Number(i)]?modules[Number(i)].title:'Módulo',area:modules[Number(i)]?modules[Number(i)].area:'Formación',text:r.note,createdAt:r.updatedAt||'Anterior',updatedAt:r.updatedAt||'Anterior',status:'pending',answer:'',answeredAt:null})}});localStorage.setItem(KEY,JSON.stringify(x));return x;}}catch(e){}return blankState()}",
    'state migration'
)

replace_once(
    "function addAlert(area,message,source){state.alerts.push({id:Date.now()+Math.random(),area,message,source,date:stamp()});save()}",
    "function addAlert(area,message,source){state.alerts.push({id:Date.now()+Math.random(),area,message,source,date:stamp()});save()}\nfunction latestQuestionForModule(i){return state.questions.slice().reverse().find(q=>q.moduleIndex===i)||null}\nfunction pendingQuestions(){return state.questions.filter(q=>q.status!=='resolved')}",
    'question helpers'
)

replace_once(
    "$('lessonNote').value=r.note||'';$('lessonNoteFeedback').textContent='';show('screen-lesson')}",
    "$('lessonNote').value=r.note||'';$('lessonNoteFeedback').textContent='';const q=latestQuestionForModule(i),qs=$('lessonQuestionStatus');qs.replaceChildren();if(q){const box=document.createElement('div');box.className='notification '+(q.status==='resolved'?'good':'warn');const sm=document.createElement('small');sm.textContent=q.status==='resolved'?'Respondida · '+(q.answeredAt||''):'Enviada · '+q.createdAt+' · Pendiente de respuesta';const tx=document.createElement('div');tx.textContent=q.text;box.append(sm,tx);if(q.status==='resolved'&&q.answer){const ans=document.createElement('div');ans.className='question-answer';ans.textContent='Respuesta del responsable: '+q.answer;box.append(ans)}qs.append(box)}show('screen-lesson')}",
    'employee question status'
)

replace_once(
    "function renderManager(){const pct=trainingPercent(),avg=latestEvalAverage();$('managerEmployeeName').textContent=state.employee.name;$('managerEmployeeMeta').textContent=state.employee.role+' · Día '+state.employee.day+' de 30';$('managerStatus').textContent=avg&&avg>=3?'Evolución adecuada':'En seguimiento';$('managerTrainingMetric').textContent=pct+'%';$('managerEvalMetric').textContent=avg?avg.toFixed(1)+'/4':'—';$('managerObsMetric').textContent=state.observations.length;$('managerAlertsMetric').textContent=unresolvedAlerts();$('managerProgressText').textContent=pct+'%';$('managerProgressBar').style.width=pct+'%';\n const areas=$('managerAreas');",
    "function renderManager(){const pct=trainingPercent(),avg=latestEvalAverage();$('managerEmployeeName').textContent=state.employee.name;$('managerEmployeeMeta').textContent=state.employee.role+' · Día '+state.employee.day+' de 30';$('managerStatus').textContent=avg&&avg>=3?'Evolución adecuada':'En seguimiento';$('managerTrainingMetric').textContent=pct+'%';$('managerEvalMetric').textContent=avg?avg.toFixed(1)+'/4':'—';$('managerObsMetric').textContent=state.observations.length;$('managerAlertsMetric').textContent=unresolvedAlerts();$('managerProgressText').textContent=pct+'%';$('managerProgressBar').style.width=pct+'%';\n const pq=pendingQuestions();$('managerQuestionsCount').textContent=pq.length+' '+(pq.length===1?'pendiente':'pendientes');const qh=$('managerQuestions');qh.replaceChildren();const ordered=state.questions.slice().reverse();if(!ordered.length){const empty=document.createElement('div');empty.className='card muted';empty.textContent='No hay dudas enviadas por el empleado.';qh.append(empty)}ordered.forEach(q=>{const d=document.createElement('div');d.className='card question-card '+(q.status==='resolved'?'resolved':'');const head=document.createElement('div');head.className='question-head';const left=document.createElement('div');const title=document.createElement('strong');title.textContent=(q.moduleIndex!==undefined&&modules[q.moduleIndex]?'Día '+modules[q.moduleIndex].day+' · '+modules[q.moduleIndex].title:q.moduleTitle||'Formación');const meta=document.createElement('small');meta.className='muted';meta.textContent=state.employee.name+' · '+(q.createdAt||'');left.append(title,document.createElement('br'),meta);const status=document.createElement('span');status.className='status question-status';status.textContent=q.status==='resolved'?'Resuelta':'Pendiente';head.append(left,status);const text=document.createElement('p');text.textContent=q.text;d.append(head,text);if(q.status==='resolved'){const ans=document.createElement('div');ans.className='question-answer';ans.textContent='Respuesta: '+(q.answer||'Sin texto');d.append(ans)}else{const ta=document.createElement('textarea');ta.className='control';ta.rows=2;ta.maxLength=300;ta.placeholder='Responder al empleado...';const btn=document.createElement('button');btn.type='button';btn.className='btn btn-primary btn-full';btn.style.marginTop='9px';btn.textContent='Responder y marcar como resuelta';btn.addEventListener('click',()=>{const answer=ta.value.trim();if(!answer){ta.focus();return}q.answer=answer;q.status='resolved';q.answeredAt=stamp();q.updatedAt=q.answeredAt;const m=modules[q.moduleIndex];addAlert(m?m.area:q.area||'Comunicación','Tu responsable respondió a tu duda: '+answer,'Respuesta del responsable');save();renderManager()});d.append(ta,btn)}qh.append(d)});\n const areas=$('managerAreas');",
    'manager question renderer'
)

replace_once(
    "state.evaluations.forEach(e=>events.push({date:e.date,title:'Evaluación · '+e.average.toFixed(1)+'/4',text:'Seguimiento registrado'}));events.slice().reverse().slice(0,8).forEach",
    "state.evaluations.forEach(e=>events.push({date:e.date,title:'Evaluación · '+e.average.toFixed(1)+'/4',text:'Seguimiento registrado'}));state.questions.forEach(q=>{events.push({date:q.createdAt,title:'Duda del empleado',text:q.text});if(q.status==='resolved'&&q.answeredAt)events.push({date:q.answeredAt,title:'Duda resuelta',text:q.answer})});events.slice().reverse().slice(0,8).forEach",
    'questions in timeline'
)

replace_once(
    "$('lessonPracticed').addEventListener('change',e=>{state.employee.activities[currentLesson]={...record(currentLesson),practiced:e.target.checked,updatedAt:stamp()};save();});$('saveLessonNote').addEventListener('click',()=>{state.employee.activities[currentLesson]={...record(currentLesson),note:$('lessonNote').value.trim(),updatedAt:stamp()};save();$('lessonNoteFeedback').textContent='Nota guardada.';$('lessonNoteFeedback').className='feedback success'});",
    "$('lessonPracticed').addEventListener('change',e=>{state.employee.activities[currentLesson]={...record(currentLesson),practiced:e.target.checked,updatedAt:stamp()};save();});$('saveLessonNote').addEventListener('click',()=>{const text=$('lessonNote').value.trim();if(!text){$('lessonNoteFeedback').textContent='Escribe la duda antes de enviarla.';$('lessonNoteFeedback').className='feedback error';return}const now=stamp(),m=modules[currentLesson];state.employee.activities[currentLesson]={...record(currentLesson),note:text,updatedAt:now};let q=state.questions.slice().reverse().find(q=>q.moduleIndex===currentLesson&&q.status!=='resolved');if(q){q.text=text;q.updatedAt=now}else{state.questions.push({id:Date.now()+Math.random(),employeeId:state.employee.id,moduleIndex:currentLesson,moduleTitle:m.title,area:m.area,text,createdAt:now,updatedAt:now,status:'pending',answer:'',answeredAt:null})}save();openLesson(currentLesson);$('lessonNoteFeedback').textContent='Duda enviada al responsable.';$('lessonNoteFeedback').className='feedback success'});",
    'send question action'
)

if s == original:
    raise SystemExit('No changes produced')
p.write_text(s, encoding='utf-8')
print(f'Patched index.html: {len(original)} -> {len(s)} bytes')
