(function(){
  'use strict';
  const STORAGE_KEY='onboarding_hosteleria_responsable_mvp_v1';
  const initialData={
    staff:[
      {id:'juan',name:'Juan Pérez',role:'Camarero sala',day:15,training:72,status:'Evolución positiva',areas:{Producto:[1,2,3],Servicio:[2,3,3],Comunicación:[2,2,3],Anticipación:[1,2,2],'Trabajo en equipo':[3,3,4]},observations:[{type:'Positivo',area:'Servicio',note:'Buena gestión de una reclamación.',date:'Hoy'},{type:'A mejorar',area:'Anticipación',note:'Preparar reposición antes del pico.',date:'Ayer'}]},
      {id:'laura',name:'Laura García',role:'Ayudante sala',day:7,training:58,status:'En desarrollo',areas:{Producto:[1,2],Servicio:[2,3],Comunicación:[2,2],Anticipación:[2,2],'Trabajo en equipo':[3,3]},observations:[{type:'A mejorar',area:'Producto',note:'Reforzar carta y alérgenos.',date:'Hoy'}]},
      {id:'pedro',name:'Pedro López',role:'Camarero barra',day:30,training:96,status:'Onboarding completado',areas:{Producto:[2,3,4],Servicio:[2,3,4],Comunicación:[3,3,4],Anticipación:[2,3,4],'Trabajo en equipo':[3,4,4]},observations:[{type:'Positivo',area:'Trabajo en equipo',note:'Apoya al resto sin indicación.',date:'Ayer'}]}
    ], evaluations:[]
  };
  let data=loadData();
  let currentId=data.staff[0].id;
  let previousScreen='home';

  const $=id=>document.getElementById(id);
  const screens=['home','person','observe','evaluate'];
  const criteria=['Conocimiento de producto','Mise en place','Comunicación','Anticipación','Trabajo en equipo','Adaptación al sistema'];

  function deepClone(v){return JSON.parse(JSON.stringify(v));}
  function loadData(){
    try{const raw=localStorage.getItem(STORAGE_KEY);if(!raw)return deepClone(initialData);const parsed=JSON.parse(raw);if(!parsed||!Array.isArray(parsed.staff))throw new Error('bad data');return parsed;}catch(e){return deepClone(initialData);}
  }
  function saveData(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(data));return true;}catch(e){return false;}}
  function getCurrent(){return data.staff.find(x=>x.id===currentId)||data.staff[0];}
  function setActiveNav(screen){document.querySelectorAll('[data-nav]').forEach(b=>b.classList.toggle('active',b.dataset.nav===screen));}
  function show(screen){
    screens.forEach(x=>$('screen-'+x).classList.toggle('hidden',x!==screen));
    if(screen==='person')renderPerson();
    if(screen==='evaluate')renderEvaluation();
    setActiveNav(screen==='person'?'home':screen);
    window.scrollTo({top:0,behavior:'auto'});
  }

  function renderEmployees(){
    const box=$('employeeList');box.innerHTML='';
    data.staff.forEach(s=>{
      const b=document.createElement('button');
      b.type='button';b.className='employee-card';
      b.innerHTML='<div class="employee-top"><div><div class="employee-name"></div><div class="muted employee-meta"></div></div><span class="status-pill"></span></div><div class="progress"><span></span></div><div class="muted progress-copy" style="margin-top:6px"></div>';
      b.querySelector('.employee-name').textContent=s.name;
      b.querySelector('.employee-meta').textContent=s.role+' · Día '+s.day+' de 30';
      b.querySelector('.status-pill').textContent=s.status;
      b.querySelector('.progress span').style.width=s.training+'%';
      b.querySelector('.progress-copy').textContent=s.training+'% formación';
      b.addEventListener('click',()=>{currentId=s.id;previousScreen='home';show('person');});
      box.appendChild(b);
    });
    fillEmployeeSelect();
  }

  function renderPerson(){
    const s=getCurrent();
    $('personName').textContent=s.name;
    $('personMeta').textContent=s.role+' · Día '+s.day+' de 30';
    $('personStatus').textContent=s.status;
    $('personProgressText').textContent=s.training+'%';
    $('personProgressBar').style.width=s.training+'%';
    const areas=$('personAreas');areas.innerHTML='';
    Object.entries(s.areas).forEach(([name,values])=>{
      const first=values[0],last=values[values.length-1];
      const arrow=last>first?'↑':last<first?'↓':'→';
      const d=document.createElement('div');d.className='area-card';
      const row=document.createElement('div');row.className='area-row';
      const n=document.createElement('span');n.className='area-name';n.textContent=name;
      const t=document.createElement('span');t.className='trend';t.textContent=values.join(' → ')+' '+arrow;
      row.append(n,t);d.appendChild(row);areas.appendChild(d);
    });
    const obs=$('personObservations');obs.innerHTML='';
    if(!s.observations.length){const x=document.createElement('div');x.className='muted';x.textContent='Todavía no hay observaciones.';obs.appendChild(x);}
    s.observations.slice(0,8).forEach(o=>{
      const d=document.createElement('div');
      const cls=o.type==='Positivo'?'positive':o.type==='Incidencia'?'incident':'improve';
      d.className='observation-card '+cls;
      const meta=document.createElement('div');meta.className='observation-meta';meta.textContent=o.type+' · '+o.area+' · '+o.date;
      const tx=document.createElement('div');tx.className='observation-text';tx.textContent=o.note;
      d.append(meta,tx);obs.appendChild(d);
    });
  }

  function fillEmployeeSelect(){
    const select=$('observationEmployee');
    const value=select.value;
    select.innerHTML='';
    data.staff.forEach(s=>{const o=document.createElement('option');o.value=s.id;o.textContent=s.name;select.appendChild(o);});
    select.value=data.staff.some(s=>s.id===value)?value:currentId;
  }

  function openObservation(from){
    previousScreen=from;
    fillEmployeeSelect();
    $('observationEmployee').value=currentId;
    $('observationMessage').textContent='';
    $('observationMessage').className='feedback';
    show('observe');
  }

  function renderEvaluation(){
    const s=getCurrent();
    $('evaluationTitle').textContent=s.name+' · Día '+s.day;
    const form=$('evaluationForm');form.innerHTML='';
    criteria.forEach((c,i)=>{
      const fs=document.createElement('fieldset');fs.className='evaluation-card';
      const legend=document.createElement('legend');legend.textContent=c;fs.appendChild(legend);
      const ratings=document.createElement('div');ratings.className='ratings';
      [1,2,3,4].forEach(n=>{
        const label=document.createElement('label');label.className='rating';
        const input=document.createElement('input');input.type='radio';input.name='q'+i;input.value=String(n);input.required=true;
        label.append(input,document.createTextNode(' '+n));ratings.appendChild(label);
      });
      fs.appendChild(ratings);form.appendChild(fs);
    });
    const noteLabel=document.createElement('label');noteLabel.className='field-label';noteLabel.htmlFor='evaluationNote';noteLabel.textContent='Comentario general (opcional)';
    const note=document.createElement('textarea');note.id='evaluationNote';note.className='control';note.rows=3;note.maxLength=220;note.placeholder='Resumen breve de la evaluación.';
    const submit=document.createElement('button');submit.type='submit';submit.className='btn btn-primary full';submit.textContent='Guardar evaluación';
    form.append(noteLabel,note,submit);
    $('evaluationMessage').textContent='';$('evaluationMessage').className='feedback';
  }

  $('quickAddBtn').addEventListener('click',()=>openObservation('home'));
  $('personObservationBtn').addEventListener('click',()=>openObservation('person'));
  $('personEvaluationBtn').addEventListener('click',()=>{previousScreen='person';show('evaluate');});
  $('observationBackBtn').addEventListener('click',()=>show(previousScreen));
  $('evaluationBackBtn').addEventListener('click',()=>show('person'));
  document.querySelectorAll('[data-go="home"]').forEach(b=>b.addEventListener('click',()=>show('home')));
  document.querySelectorAll('[data-nav]').forEach(b=>b.addEventListener('click',()=>{
    const target=b.dataset.nav;
    if(target==='home')show('home');
    if(target==='observe')openObservation('home');
    if(target==='evaluate'){previousScreen='home';show('evaluate');}
  }));

  $('observationNote').addEventListener('input',e=>$('noteCounter').textContent=e.target.value.length);
  $('observationForm').addEventListener('submit',e=>{
    e.preventDefault();
    const id=$('observationEmployee').value;
    const note=$('observationNote').value.trim();
    const type=(new FormData(e.currentTarget)).get('observationType');
    const area=$('observationArea').value;
    const msg=$('observationMessage');
    if(!id||!type||!area||!note){msg.textContent='Completa los campos obligatorios.';msg.className='feedback error';return;}
    const employee=data.staff.find(s=>s.id===id);
    if(!employee){msg.textContent='No se ha encontrado el empleado.';msg.className='feedback error';return;}
    employee.observations.unshift({type,area,note,date:'Ahora'});
    currentId=id;saveData();renderEmployees();renderPerson();
    $('observationNote').value='';$('noteCounter').textContent='0';
    msg.textContent='Observación guardada correctamente.';msg.className='feedback success';
  });

  $('evaluationForm').addEventListener('submit',e=>{
    e.preventDefault();
    const form=e.currentTarget;
    if(!form.checkValidity()){form.reportValidity();return;}
    const fd=new FormData(form);
    const scores=criteria.map((c,i)=>({criterion:c,score:Number(fd.get('q'+i))}));
    data.evaluations.push({employeeId:currentId,date:new Date().toISOString(),scores,note:($('evaluationNote')||{}).value||''});
    saveData();
    $('evaluationMessage').textContent='Evaluación guardada correctamente.';
    $('evaluationMessage').className='feedback success';
  });

  $('resetDemoBtn').addEventListener('click',()=>{
    if(!confirm('¿Restablecer todos los datos de prueba?'))return;
    data=deepClone(initialData);currentId=data.staff[0].id;saveData();renderEmployees();show('home');
  });

  renderEmployees();show('home');

  if('serviceWorker' in navigator){window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(()=>{}));}
})();
