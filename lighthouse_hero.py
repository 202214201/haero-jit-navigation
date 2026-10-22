"""해로(海路) 라이트/야간모드 등대 표지. 이미지 파일 없이 SVG로 그립니다."""

import streamlit.components.v1 as components


def draw_lighthouse(theme="light"):
    """theme='light' 또는 'dark'. 색상과 애니메이션이 포함된 반응형 메인 표지."""
    mode = "night" if theme == "dark" else "day"
    html = r'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body>
<style>
  * { box-sizing: border-box; }
  html, body { padding: 0; margin: 0; width: 100%; overflow: hidden;
    font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif; }
  .scene { height: 365px; border-radius: 18px; overflow: hidden; position: relative;
    box-shadow: 0 8px 28px rgba(0, 37, 82, .13); isolation: isolate; }
  .scene svg { display: block; width: 100%; height: 100%; }
  .scene.day   { color: #0b3463; background: #a3d6ff; }
  .scene.night { color: #edf5ff; background: #091a3a; }
  .night-only, .scene.night .day-only { display: none; }
  .scene.night .night-only { display: initial; }
  .copy { position: absolute; top: 17%; left: 39%; right: 4%; text-shadow: 0 1px 6px rgba(255,255,255,.2); }
  .night .copy { text-shadow: 0 2px 8px rgba(0,0,0,.4); }
  .eyebrow { display: inline-block; font-size: 12px; font-weight: 800;
    letter-spacing: 2px; opacity: .8; margin-bottom: 7px; }
  .copy h2 { margin: 0 0 4px; font-size: clamp(39px,5vw,64px); line-height: 1.17;
    font-weight: 900; letter-spacing: -3px; }
  .copy h2 small { font-size: .49em; font-weight: 600; opacity: .75; letter-spacing: 0; }
  .copy p { margin: 10px 0 16px; font-size: clamp(14px,1.7vw,21px);
    font-weight: 650; line-height: 1.6; }
  .copy .sub { font-size: 13px; font-weight: 500; opacity: .83; }
  .tags { display:flex; gap:8px; flex-wrap:wrap; margin-top: 10px; }
  .tags span { border:1px solid currentColor; padding:5px 9px; border-radius: 999px;
    font-size: 11px; font-weight: 650; background:rgba(255,255,255,.18); }
  .night .tags span { background:rgba(255,255,255,.06); }
  .lamp-ray { transform-origin: 178px 149px; animation: sweep 8s ease-in-out infinite alternate; }
  .night .lamp-ray { opacity: .95; } .day .lamp-ray { opacity: .18; }
  .wave1 { animation: drift 6s ease-in-out infinite alternate; }
  .wave2 { animation: drift 8s ease-in-out infinite alternate-reverse; }
  .cloud { animation: clouds 16s ease-in-out infinite alternate; }
  .stars circle { animation: twinkle 3s ease-in-out infinite alternate; }
  @keyframes sweep { from { transform:rotate(-7deg); } to { transform:rotate(7deg); } }
  @keyframes drift { from { transform:translateX(-9px); } to { transform:translateX(13px); } }
  @keyframes clouds { from { transform:translateX(-10px); } to { transform:translateX(24px); } }
  @keyframes twinkle { from { opacity:.25; } to { opacity:1; } }
  @media(max-width:620px) {
    .scene { height: 295px; border-radius: 12px; }
    .copy { left: 41%; right: 3%; top: 19%; }
    .eyebrow { font-size: 9px; letter-spacing: .6px; }
    .copy h2 { font-size: 35px; letter-spacing: -2px; }
    .copy p { font-size: 12px; margin: 7px 0; }
    .copy .sub { font-size: 10px; }
    .tags { display:none; }
  }
  @media(prefers-reduced-motion: reduce) {
    .lamp-ray,.wave1,.wave2,.cloud,.stars circle { animation:none !important; }
  }
</style>
<div class="scene THEME" role="img" aria-label="등대와 컨테이너선이 있는 항구, 낮과 밤 테마가 바뀌는 해로 표지">
  <svg viewBox="0 0 1200 420" preserveAspectRatio="xMinYMid slice" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="daySky" x2="0" y2="1"><stop stop-color="#7fc6ff"/><stop offset="1" stop-color="#eef9ff"/></linearGradient>
      <linearGradient id="nightSky" x2="0" y2="1"><stop stop-color="#06132e"/><stop offset="1" stop-color="#16365d"/></linearGradient>
      <linearGradient id="water" x2="0" y2="1"><stop stop-color="#3d9cd4"/><stop offset="1" stop-color="#0e5b9f"/></linearGradient>
      <linearGradient id="darkWater" x2="0" y2="1"><stop stop-color="#133b68"/><stop offset="1" stop-color="#061a35"/></linearGradient>
      <linearGradient id="shine"><stop stop-color="#ffdf79" stop-opacity=".75"/><stop offset="1" stop-color="#fff1ab" stop-opacity="0"/></linearGradient>
      <radialGradient id="glow"><stop stop-color="#fffadd" stop-opacity=".95"/><stop offset="1" stop-color="#ffed90" stop-opacity="0"/></radialGradient>
    </defs>
    <rect class="day-only" width="1200" height="420" fill="url(#daySky)"/>
    <rect class="night-only" width="1200" height="420" fill="url(#nightSky)"/>
    <g class="stars night-only" fill="#e8f5ff">
      <circle cx="58" cy="27" r="1.5"/><circle cx="304" cy="50" r="1.5"/><circle cx="404" cy="18" r="1"/>
      <circle cx="560" cy="58" r="2"/><circle cx="681" cy="25" r="1.5"/><circle cx="835" cy="56" r="1"/>
      <circle cx="963" cy="19" r="1.5"/><circle cx="1155" cy="76" r="1.5"/><circle cx="1064" cy="119" r="1"/>
      <circle cx="767" cy="99" r="1"/><circle cx="337" cy="104" r="1.1"/>
    </g>
    <circle class="day-only" cx="1089" cy="85" r="37" fill="#fff6c1" opacity=".82"/>
    <circle class="night-only" cx="1093" cy="65" r="24" fill="#faf4d5"/>
    <circle class="night-only" cx="1102" cy="56" r="24" fill="#091a3a"/>
    <g class="cloud day-only" fill="#fff" opacity=".69">
      <path d="M12 108q29-46 63-13q26-27 54 7q33-16 56 17H0Z"/>
      <path d="M862 143q19-32 47-14q17-32 52-13q30-21 51 27Z"/>
    </g>
    <path class="day-only" d="M0 264Q145 175 313 244T615 246T880 220T1200 256V350H0Z" fill="#a5c8d5"/>
    <path class="night-only" d="M0 262Q170 173 335 234T615 243T872 207T1200 249V340H0Z" fill="#0d2643"/>
    <!-- coastal city and terminal -->
    <g fill="#7394b3" opacity=".7" class="day-only">
      <rect x="403" y="238" width="18" height="56"/><rect x="428" y="247" width="31" height="46"/>
      <rect x="468" y="222" width="18" height="70"/><rect x="496" y="245" width="31" height="45"/>
      <rect x="1080" y="236" width="21" height="58"/><rect x="1110" y="217" width="37" height="75"/>
      <rect x="1158" y="242" width="30" height="50"/>
    </g>
    <g fill="#345676" opacity=".7" class="night-only">
      <rect x="403" y="238" width="18" height="56"/><rect x="428" y="247" width="31" height="46"/>
      <rect x="468" y="222" width="18" height="70"/><rect x="496" y="245" width="31" height="45"/>
      <rect x="1080" y="236" width="21" height="58"/><rect x="1110" y="217" width="37" height="75"/>
      <rect x="1158" y="242" width="30" height="50"/>
    </g>
    <rect y="290" width="1200" height="130" class="day-only" fill="url(#water)"/>
    <rect y="290" width="1200" height="130" class="night-only" fill="url(#darkWater)"/>
    <!-- cranes -->
    <g stroke="#3771a5" stroke-width="6" fill="none" stroke-linejoin="round">
      <path d="M816 291V214L842 189L868 214V291M842 189V174M842 198H1004M910 198V252M981 198V259"/>
      <path d="M1020 290V230L1041 211L1063 230V290M1041 211V196M1041 221H1150M1100 221V258"/>
    </g>
    <g class="night-only" stroke="#f9bd67" stroke-width="3"><path d="M842 189H1004M1041 211H1150"/></g>
    <!-- ship -->
    <g transform="translate(660,265)">
      <path d="M0 17H430L397 50H36Z" fill="#153961"/>
      <path d="M18 18H411" stroke="#fff5e0" stroke-width="3"/>
      <rect x="73" y="-23" width="54" height="39" rx="2" fill="#da8658"/>
      <rect x="131" y="-23" width="54" height="39" rx="2" fill="#e9ad64"/>
      <rect x="189" y="-23" width="54" height="39" rx="2" fill="#387cab"/>
      <rect x="247" y="-23" width="54" height="39" rx="2" fill="#d16c51"/>
      <rect x="104" y="-65" width="54" height="40" rx="2" fill="#c95e4e"/>
      <rect x="162" y="-65" width="54" height="40" rx="2" fill="#eab36a"/>
      <rect x="220" y="-65" width="54" height="40" rx="2" fill="#396e9f"/>
      <rect x="278" y="-23" width="35" height="39" rx="2" fill="#c68e6c"/>
      <rect x="322" y="-40" width="60" height="57" rx="3" fill="#f3f0df"/>
      <rect x="334" y="-31" width="11" height="10" fill="#246190"/><rect x="352" y="-31" width="11" height="10" fill="#246190"/>
      <path d="M360 -40V-55" stroke="#ccd6df" stroke-width="3"/>
      <g stroke="#1c3e66" opacity=".55" stroke-width="1">
        <path d="M88 -21V16M145 -21V16M203 -21V16M262 -21V16"/>
        <path d="M117 -63V-24M175 -63V-24M232 -63V-24"/>
      </g>
    </g>
    <!-- lighthouse rocks -->
    <path d="M0 373L30 324L93 305L139 325L184 296L233 313L284 355L351 369L392 420H0Z" fill="#425b77"/>
    <path d="M0 409L51 356L106 364L155 345L206 379L244 362L301 398L342 385L385 420H0Z" fill="#294561"/>
    <path class="day-only" d="M0 403L56 362L95 386L141 354L186 389L241 377L303 418H0Z" fill="#77929d"/>
    <!-- lighthouse shaft -->
    <path d="M137 171H216L241 329H109Z" fill="#f6f8f7" stroke="#264d77" stroke-width="3"/>
    <path d="M129 257L225 257L234 291L118 291Z" fill="#287bc0"/>
    <path d="M139 185L212 185L217 207L136 207Z" fill="#287bc0"/>
    <rect x="169" y="220" width="17" height="33" rx="8" fill="#204f80"/>
    <path d="M161 329V307Q161 287 176 287Q193 287 193 307V329" fill="#173b66" stroke="#6b93bd" stroke-width="3"/>
    <!-- lighthouse gallery and roof -->
    <rect x="135" y="139" width="84" height="40" rx="3" fill="#123d70"/>
    <rect x="145" y="140" width="66" height="35" fill="#ffd978"/>
    <g stroke="#183f70" stroke-width="5"><path d="M160 139V177M177 139V177M194 139V177"/></g>
    <path d="M128 137Q135 106 177 105Q218 106 226 137Z" fill="#1762a7" stroke="#113969" stroke-width="4"/>
    <rect x="122" y="175" width="108" height="12" rx="4" fill="#1d5a95"/>
    <path d="M117 165H237M128 165V184M147 165V184M209 165V184M230 165V184" stroke="#2c6199" stroke-width="4"/>
    <path d="M177 105V89" stroke="#1a4178" stroke-width="5"/><circle cx="177" cy="87" r="7" fill="#2669ae"/>
    <!-- active lighthouse beam -->
    <g class="lamp-ray">
      <path d="M181 146L720 58L730 221Z" fill="url(#shine)"/>
    </g>
    <circle cx="178" cy="151" r="25" fill="url(#glow)"/>
    <!-- moving waves -->
    <path class="wave1" d="M-20 337Q50 322 121 342T264 338T410 345T570 338T743 348T911 335T1090 345T1220 335" fill="none" stroke="#c4efff" stroke-width="5" opacity=".72"/>
    <path class="wave2" d="M-20 371Q60 358 143 376T305 373T466 377T640 368T810 378T1010 366T1220 377" fill="none" stroke="#85d6fc" stroke-width="6" opacity=".61"/>
    <path d="M0 408Q180 391 342 405T660 404T940 400T1200 407" fill="none" stroke="#e0f7ff" stroke-width="3" opacity=".44"/>
    <g class="night-only" stroke="#ffc57c" opacity=".6">
      <path d="M680 329h36m50 17h65m86-11h57m58 10h38m-174 38h86m-400-19h45"/>
    </g>
  </svg>
  <div class="copy">
    <span class="eyebrow">NEXUS · SMART PORT NAVIGATION</span>
    <h2>해로 <small>海路</small></h2>
    <p>AI로 더 똑똑하게,<br>대기 없이 항구로.</p>
    <div class="sub">JIT 입항 · 친환경 운항 · 스마트 항만</div>
    <div class="tags"><span>혼잡도 예측</span><span>E-co로</span><span>입항 예약</span><span>입항 가이드</span></div>
  </div>
</div>
</body></html>'''.replace("THEME", mode)
    components.html(html, height=373, scrolling=False)
