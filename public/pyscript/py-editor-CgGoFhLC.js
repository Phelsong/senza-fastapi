import{T as t,d as e,a as r,o as n,X as o,H as s,s as i}from"./core-Bao2B1pB.js";let a=0;const c=t=>`${t}-editor-${a++}`,l=new Map,u=new Map,d={worker:{codeBeforeRun:()=>i,onReady:({runAsync:t,io:e},{sync:r})=>{e.stdout=e.buffered(r.write),e.stderr=e.buffered(r.writeErr),r.revoke(),r.runAsync=t}}};async function p({currentTarget:t}){const{env:e,pySrc:r,outDiv:i}=this,a=!!t;if(a&&(t.disabled=!0,i.innerHTML=""),!l.has(e)){const t=URL.createObjectURL(new Blob([""])),r={type:this.interpreter},{config:i}=this;if(i){r.configURL=i;const{parse:t}=i.endsWith(".toml")?await import("./toml-CvAfdf9_.js"):JSON;r.config=t(await fetch(i).then((t=>t.text()))),r.version=n(r.config)}else r.config={};const a=o.call(new s(null,d),t,r),{sync:c}=a,{promise:u,resolve:p}=Promise.withResolvers();l.set(e,u),c.revoke=()=>{URL.revokeObjectURL(t),p(a)}}return l.get(e).then((e=>{e.onerror=({error:t})=>{a&&(i.innerHTML+=`<span style='color:red'>${t.message||t}</span>\n`),console.error(t)};const n=()=>{a&&(t.disabled=!1)},{sync:o}=e;o.write=t=>{a&&(i.innerText+=`${t}\n`)},o.writeErr=t=>{a&&(i.innerHTML+=`<span style='color:red'>${t}</span>\n`)},o.runAsync(r).then(n,n)}))}const m=(t,e)=>{const r=document.createElement("div");r.className=`${e}-editor-input`,r.setAttribute("aria-label","Python Script Area");const n=((t,e)=>{const r=document.createElement("button");return r.className=`absolute ${e}-editor-run-button`,r.innerHTML='<svg style="height:20px;width:20px;vertical-align:-.125em;transform-origin:center;overflow:visible;color:green" viewBox="0 0 384 512" aria-hidden="true" role="img" xmlns="http://www.w3.org/2000/svg"><g transform="translate(192 256)" transform-origin="96 0"><g transform="translate(0,0) scale(1,1)"><path d="M361 215C375.3 223.8 384 239.3 384 256C384 272.7 375.3 288.2 361 296.1L73.03 472.1C58.21 482 39.66 482.4 24.52 473.9C9.377 465.4 0 449.4 0 432V80C0 62.64 9.377 46.63 24.52 38.13C39.66 29.64 58.21 29.99 73.03 39.04L361 215z" fill="currentColor" transform="translate(-192 -256)"></path></g></g></svg>',r.setAttribute("aria-label","Python Script Run Button"),r.addEventListener("click",t),r})(t,e),o=document.createElement("div");return o.addEventListener("keydown",(t=>{t.stopPropagation()})),r.append(n,o),r},f=(t,e)=>{const r=document.createElement("div");r.className=`${e}-editor-box`;const n=m(t,e),o=(t=>{const e=document.createElement("div");return e.className=`${t}-editor-output`,e.id=`${c(t)}-output`,e})(e);return r.append(n,o),[r,o]},g=async(t,n,o)=>{const[{basicSetup:s,EditorView:i},{Compartment:a},{python:l},{indentUnit:d},{keymap:m},{defaultKeymap:g}]=await Promise.all([import("./codemirror-Cuc1ujlq.js"),import("./codemirror_state-D1qTXrff.js"),import("./codemirror_lang-python-CJNnzWx3.js"),import("./codemirror_language-w-S9uYcH.js").then((function(t){return t.x})),import("./codemirror_view-DfjLm8GV.js").then((function(t){return t.q})),import("./codemirror_commands-DrGPggEa.js")]);let h=t.hasAttribute("setup");const v=t.hasAttribute("config"),b=`${o}-${t.getAttribute("env")||c(n)}`;if(v&&u.has(b))throw new SyntaxError(u.get(b)?`duplicated config for env: ${b}`:`unable to add a config to the env: ${b}`);u.set(b,v);let y=t.src?await fetch(t.src).then((t=>t.text())):t.textContent;const w={interpreter:o,env:b,config:v&&new URL(t.getAttribute("config"),location.href).href,get pySrc(){return h?y:T.state.doc.toString()},get outDiv(){return h?null:S}};let E;e(t,{target:{get:()=>E},code:{get:()=>w.pySrc,set:t=>{h||T.update([T.state.update({changes:{from:0,to:T.state.doc.length,insert:t}})])}},process:{value(t){const e=h,r=y;h=!0,y=t;const n=()=>{h=e,y=r};return p.call(w,{currentTarget:null}).then(n,n)}}});const $=()=>{const e=new Event(`${n}-editor`,{bubbles:!0});t.dispatchEvent(e)};if(h)return await p.call(w,{currentTarget:null}),void $();const x=t.getAttribute("target");if(x){if(E=document.getElementById(x)||document.querySelector(x),!E)throw new Error(`Unknown target ${x}`)}else E=document.createElement(`${n}-editor`),E.style.display="block",t.after(E);E.id||(E.id=c(n)),E.hasAttribute("exec-id")||E.setAttribute("exec-id",0),E.hasAttribute("root")||E.setAttribute("root",E.id);const A=p.bind(w),[L,S]=f(A,n);L.dataset.env=t.hasAttribute("env")?b:o;const C=L.querySelector(`.${n}-editor-input > div`).attachShadow({mode:"open"});C.innerHTML="<style> :host { all: initial; }</style>",E.appendChild(L);const k=r(t.textContent).trim(),R=/^(\s+)/m.test(k)?RegExp.$1:"    ",T=new i({extensions:[d.of(R),(new a).of(l()),m.of([...g,{key:"Ctrl-Enter",run:A,preventDefault:!0},{key:"Cmd-Enter",run:A,preventDefault:!0},{key:"Shift-Enter",run:A,preventDefault:!0}]),s],parent:C,doc:k});T.focus(),$()};let h=0,v=Promise.resolve();const b=()=>{h=0,y()},y=()=>{if(!h){h=setTimeout(b,250);for(const[e,r]of t){const t=`script[type="${e}-editor"]`;for(const n of document.querySelectorAll(t))n.type+="-active",v=v.then((()=>g(n,e,r)))}return v}};new MutationObserver(y).observe(document,{childList:!0,subtree:!0});var w=y();export{w as default};
//# sourceMappingURL=py-editor-CgGoFhLC.js.map
