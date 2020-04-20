(this.webpackJsonpclient=this.webpackJsonpclient||[]).push([[0],{118:function(e,t,a){e.exports=a.p+"static/media/stocks.456ede4e.jpg"},183:function(e,t,a){e.exports=a(216)},194:function(e,t,a){},197:function(e,t,a){},216:function(e,t,a){"use strict";a.r(t);var n,r,l=a(0),o=a.n(l),i=a(12),c=a.n(i),s=a(113),u=a(32),m=a(264),d=a(245),h=a(246),f=a(247),p=a(82),g=(a(194),function(){return o.a.createElement(m.a,{open:!0,variant:"permanent",anchor:"left",className:"Sidebar"},o.a.createElement(d.a,null,["Home","Indicators","Strategies"].map((function(e){return o.a.createElement(p.a,{to:e.toLowerCase()},o.a.createElement(h.a,{button:!0,key:e},o.a.createElement(f.a,{primary:e})))}))))}),E=(a(197),function(e){return function(t){return o.a.createElement("div",{className:"container"},o.a.createElement("div",{className:"sidebar_container"},o.a.createElement(g,null)),o.a.createElement("div",{className:"main_container"},o.a.createElement(e,t)))}}),b=E((function(){return l.createElement("div",{className:"error-pg-404"},l.createElement("h1",null,"Error 404:"),l.createElement("h3",null,"The page you requested does not exist"))})),v=a(118),y=a.n(v),x=E((function(){return o.a.createElement("div",{className:"Home"},o.a.createElement("img",{src:y.a,className:"StocksImage",style:{height:720,width:1280}}),o.a.createElement("h1",null,"Team 128: TBD"),o.a.createElement("p",null,"The goal of this visualization tool is to evaluate the effectiveness of indicators that can be implemented in machine learning models for predicting stock market prices. Key features of this tool includes:",o.a.createElement("li",null,"The ability to visually and interactively determine the effectiveness of market indicators based on historical data."),o.a.createElement("li",null,"The flexibility to investigate the performance of indicators under different market conditions."),o.a.createElement("li",null,"Present a comparison of the performance of algorithms implementing the selected indicator")))})),S=a(49),k=a.n(S),j=a(67),w=a(11),O=a(248),_=a(256),L=a(257),C=a(258),D=a(19),N=a(259),M=a(70),R=a(68),V=a.n(R),B=function(e){var t=null!==e&&void 0!==e?e:new Date,a=(t.getMonth()+1).toString(),n=t.getDate().toString(),r=t.getFullYear();return a.length<2&&(a="0"+a),n.length<2&&(n="0"+n),[r,a,n].join("-")},H=a(45),I=a(69),T=a(8),A=a(119),P=a(120),F=function(){function e(){Object(A.a)(this,e)}return Object(P.a)(e,null,[{key:"initChart",value:function(e,t,a,n,r,l,o,i,c,s,u,m){e.append("text").attr("x",o/2).attr("y",-u/3).attr("font-size","24px").attr("text-anchor","middle").text(t),e.append("text").attr("x",o/2).attr("y",i+2*u/3).attr("font-size","16px").attr("text-anchor","middle").text(a),e.append("text").attr("transform",(function(e){return"rotate(-90)"})).attr("x",-i/2).attr("y",-2*m/3).attr("font-size","16px").attr("text-anchor","middle").text(n),e.append("g").attr("transform","translate(0,"+s+")").call(T.a(r).ticks(5)),e.append("g").attr("transform","translate("+c+", 0)").attr("class","y axis").call(T.b(l))}},{key:"undefinedHandler",value:function(e,t){return e||t}},{key:"createLegend",value:function(e,t,a,n){var r=n-25*(t.length+1);t.forEach((function(t){if(t.isLine){var a=T.d().x((function(e){return e[0]})).y((function(e){return e[1]})).curve(T.c),n=[[20,r],[30,r]];e.append("path").datum(n).style("stroke",t.color).attr("stroke-width",3).style("fill","none").attr("d",a)}else e.append("circle").attr("cx",25).attr("cy",r).attr("r",6).style("fill",t.color).style("stroke",t.color),t.hollow&&e.append("circle").attr("cx",25).attr("cy",r).attr("r",4).style("fill","white").style("stroke","white");e.append("text").attr("x",35).attr("y",5+r).text(t.name).style("font-size","12px").attr("alignment-baseline","middle"),r+=25}))}}]),e}(),z=function(e){for(var t=e.data,a=e.label,n=Object(l.useRef)(null),r=50,i=100,c=50,s=100,u=t[0][0],m=t[0][0],d=t[0][1],h=t[0][1],f=1;f<t.length;f++)t[f][0]>u&&(u=t[f][0]),t[f][0]<m&&(m=t[f][0]),t[f][1]>d&&(d=t[f][1]),t[f][1]<h&&(h=t[f][1]);var p=T.h().range([0,500]).domain([m,u]),g=T.h().range([500,0]).domain([h,d]),E=function(e,a,l){var o=T.j(n.current);o.selectAll("*").remove();var i=F.undefinedHandler(T.e([0,1-d/(d-h)]),0),c=F.undefinedHandler(T.f([1,i]),1);F.initChart(o,e,"% gain","value",a,l,500,500,500*(1-F.undefinedHandler(T.f([1,u/(u-m)]),0)),500*c,r,s),function(e,a,n,r,l){e.selectAll("circle").data(t).enter().append("circle").attr("cx",(function(e){return a(e[0])})).attr("cy",(function(e){return n(e[1])})).attr("r",l).style("fill",r)}(o,a,l,"#d95f02",5)};return Object(l.useEffect)((function(){E(a,p,g)})),o.a.createElement("svg",{width:500+s+i,height:500+r+c},o.a.createElement("g",{ref:n,transform:"translate(".concat(s,",").concat(r,")")}))},K=a(249),W=a(250),$=function(e){var t=e.labels,a=e.data,n=["Pearson Coefficient","Importance Values"],r=Object(l.useRef)(null),i=50,c=0,s=50,u=225,m=T.h().range([0,150]).domain([0,F.undefinedHandler(T.e(a.map((function(e){return e[2]}))),0)]),d=T.h().range([0,150]).domain([0,F.undefinedHandler(T.e(a.map((function(e){return e[1]}))),0)]),h=T.g().range([0,250]).domain(t);return Object(l.useEffect)((function(){!function(){var e=T.j(r.current);e.selectAll("*").remove();for(var l=0;l<t.length;l++)e.append("text").attr("x",-10).attr("y",F.undefinedHandler(h(t[l]),0)+h.bandwidth()/1.9).attr("font-size","16px").attr("text-anchor","end").text(t[l]);e.append("text").attr("x",140).attr("y",-20).attr("font-size","16px").attr("text-anchor","end").text(n[0]),e.append("text").attr("x",160).attr("y",-20).attr("font-size","16px").attr("text-anchor","start").text(n[1]),e.selectAll("rect").data(a).enter().append("rect").attr("x",(function(e){return 150-d(e[1])})).attr("y",(function(e){return F.undefinedHandler(h(t[e[0]]),0)})).attr("width",(function(e){return d(e[1])})).attr("height",h.bandwidth()-2).style("fill","steelblue"),e.selectAll("rect2").data(a).enter().append("rect").attr("x",155).attr("y",(function(e){return F.undefinedHandler(h(t[e[0]]),0)})).attr("width",(function(e){return m(e[2])})).attr("height",h.bandwidth()-2).style("fill","red")}()}),[]),o.a.createElement("svg",{width:300+u+c,height:250+i+s},o.a.createElement("g",{ref:r,transform:"translate(".concat(u,",").concat(i,")")}))},J=a(263),q=a(57),Y=function(e){for(var t=e.onChange,a=e.title,n=e.description,r=e.minVal,l=e.maxVal,i=e.defaultValue,c=e.labels,s=[],u=0;u<c.length;u++)s.push({value:u,label:String(c[u]+"%")});return o.a.createElement(O.a,{item:!0,lg:2},o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(W.a,null,o.a.createElement(q.a,{id:"discrete-slider-small-steps",gutterBottom:!0},o.a.createElement("b",null,a,":")),o.a.createElement("p",null,n),o.a.createElement(J.a,{defaultValue:i,step:1,marks:s,min:r,max:l,onChange:t,valueLabelDisplay:"auto"}))))},G=a(254),Q=a(253),U=a(255),X=a(251),Z=a(262),ee={acc_dist_index:{label:"Accumulation/Distribution Index",description:"An indicator intended to relate price and volume.",more:"https://en.wikipedia.org/wiki/Accumulation/distribution_index"},chaikin_money_flow:{label:"Chaikin Money flow",description:"Measures the amount of Money Flow Volume over a specific period.",more:"http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf"},ease_of_move:{label:"Ease of Movement",description:"Relates an asset's price change to its volume and is particularly useful for assessing the strength of a trend.",more:"https://en.wikipedia.org/wiki/Ease_of_movement"},williams_r:{label:"Williams R",description:"Reflects the level of the close relative to the highest high for the look-back period. ",more:"https://school.stockcharts.com/doku.php?id=technical_indicators:williams_r"},rel_strength:{label:"Relative Strength Index",description:"Compares the magnitude of recent gains and losses over a specified time period to measure speed and change of price movements of a security.",more:"https://www.investopedia.com/terms/r/rsi.asp"}},te=function(e){var t=e.data,a=[],n=[],r=t.indicator_list,i={};Object.entries(t.indicators).forEach((function(e){var t=Object(w.a)(e,1)[0];i[t]=!0}));var c=Object(l.useState)(5),s=Object(w.a)(c,2),u=s[0],m=s[1],d=Object(l.useState)(i),h=Object(w.a)(d,2),f=h[0],p=h[1],g=function(e){p(Object(I.a)({},f,Object(H.a)({},e.target.value,e.target.checked)))};a.push(o.a.createElement(O.a,{item:!0,lg:2}));for(var E=0;E<t.f_regression.term_5.p_values.length;E++)n.push([E,t.predict.term_5.importance_values[E],t.f_regression.term_5.p_values[E]]);a.push(o.a.createElement(O.a,{item:!0,lg:4,key:"fasdklj"},o.a.createElement(K.a,{variant:"outlined"},o.a.createElement($,{labels:r.map((function(e){return ee[e].label})),data:n}),o.a.createElement("p",{style:{textAlign:"center"}},"This plot shows indicators most likely to predict future stock direction"))));var b=r.map((function(e){return o.a.createElement(X.a,{control:o.a.createElement(Z.a,{checked:f[e],onChange:g,value:e}),label:ee[e].label})}));return a.push(o.a.createElement(O.a,{item:!0,lg:2},o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(W.a,null,o.a.createElement(Q.a,{component:"fieldset"},o.a.createElement(G.a,{component:"legend"},"Select Indicators"),o.a.createElement(U.a,null,b)))))),a.push(o.a.createElement(Y,{onChange:function(e,t){"number"==typeof t&&m(t)},title:"Enter prediction term",description:"Select term to compare gain vs indicator",minVal:1,maxVal:t.dates.length-5,defaultValue:1,labels:[]})),Object.entries(t.indicators).forEach((function(e){var n=Object(w.a)(e,2),r=n[0],l=n[1];if(f[r]){for(var i=[],c=0;c<t.dates.length-u;c++)i[c]=[],i[c].push(t.cum_return[c+u]-t.cum_return[c]),i[c].push(l[c]);a.push(o.a.createElement(O.a,{item:!0,lg:4,key:r},o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(z,{data:i,label:ee[r].label})),o.a.createElement("p",{style:{textAlign:"center"}},ee[r].description),o.a.createElement("div",{className:"MoreInfo",style:{textAlign:"right"}},o.a.createElement("a",{href:ee[r].more,target:"_blank",rel:"noopener noreferrer"},"For More Info"))))}})),o.a.createElement("div",{className:"IndicatorLayout"},o.a.createElement(O.a,{container:!0,spacing:1},a))},ae=(E(te),E((function(){var e=Object(l.useState)(!1),t=Object(w.a)(e,2),a=t[0],n=t[1],r=Object(l.useState)(""),i=Object(w.a)(r,2),c=i[0],s=i[1],u=Object(l.useState)(new Date),m=Object(w.a)(u,2),d=m[0],h=m[1],f=new Date;null===f||void 0===f||f.setMonth(f.getMonth()-3);var p=Object(l.useState)(f),g=Object(w.a)(p,2),E=g[0],b=g[1],v=Object(l.useState)(),y=Object(w.a)(v,2),x=y[0],S=y[1],R=V.a.create(),H=function(){var e=Object(j.a)(k.a.mark((function e(){var t,a,r,l;return k.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return n(!0),e.next=3,R.get("/api/analysis/example",{params:{symbol:c,start_date:B(E),end_date:B(d)}});case 3:if(t=e.sent,a=t.status,r=t.statusText,l=t.data,console.log(t),200!=a){e.next=11;break}S(l),n(!1),e.next=14;break;case 11:throw n(!1),console.log(a,r),new Error(r);case 14:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return o.a.createElement("div",{className:"IndicatorPage"},o.a.createElement("h1",null,"Indicators"),o.a.createElement("p",null,"This page is used to determine which indicators are useful in a model to predict stock direction. Please enter the Stock Ticker, the Start Date, End Date and then run!"),o.a.createElement(D.a,{utils:M.a},o.a.createElement(O.a,{container:!0,justify:"space-around"},o.a.createElement(_.a,{placeholder:"Enter Stock Ticker",inputProps:{"aria-label":"description"},onChange:function(e){return s(null===e||void 0===e?void 0:e.target.value)}}),o.a.createElement(N.a,{margin:"normal",id:"date-picker-dialog",label:"Start Date",format:"MM/dd/yyyy",value:E,onChange:b,KeyboardButtonProps:{"aria-label":"change date"}}),o.a.createElement(N.a,{margin:"normal",id:"date-picker-dialog",label:"End Date",format:"MM/dd/yyyy",value:d,onChange:h,KeyboardButtonProps:{"aria-label":"change date"}}),o.a.createElement(L.a,{variant:"contained",onClick:function(){return H()},disabled:!c},"Run"))),a?o.a.createElement(C.a,{style:{alignContent:"center",height:"40px"}}):x&&o.a.createElement(te,{data:x}))}))),ne=["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00"],re=function(e){for(var t=e.data,a=e.dates,n=e.trades,r=e.labels,i=e.title,c=Object(l.useRef)(null),s=50,u=100,m=50,d=100,h=t[0][0],f=0;f<t.length;f++){var p=F.undefinedHandler(T.e(t[f]),0);p>h&&(h=p)}var g=T.i().range([0,500]).domain([F.undefinedHandler(T.f(a),0),F.undefinedHandler(T.e(a),0)]),E=T.h().range([500,0]).domain([0,h]),b=function(e,t,a){var n=T.d().x((function(e){return g(e[0])})).y((function(e){return E(e[1])})).curve(T.c);t.append("path").datum(e).style("stroke",a).attr("stroke-width",1.5).style("fill","none").attr("d",n)},v=function(e,t,a,n,r){e.selectAll(a).data(t).enter().append("circle").attr("r",5).attr("cx",(function(e){return g(e[0])})).attr("cy",(function(e){return E(e[1])})).style("fill",r),n&&e.selectAll(a+"2").data(t).enter().append("circle").attr("r",3).attr("cx",(function(e){return g(e[0])})).attr("cy",(function(e){return E(e[1])})).style("fill","white")};return Object(l.useEffect)((function(){!function(){var e=T.j(c.current);e.selectAll("*").remove(),F.initChart(e,i,"Time","Portfolio Value ($)",g,E,500,500,0,500,s,d);for(var l=0;l<t[0].length;l++){for(var o=[],u=0;u<a.length;u++)o.push([a[u],t[u][l]]);b(o,e,ne[l%ne.length])}var m=[],h=[],f=[],p=[];for(l=0;l<n.length;l++)for(u=0;u<a.length;u++)0===n[l][u]?h.push([a[u],t[u][l]]):1===n[l][u]?m.push([a[u],t[u][l]]):2===n[l][u]?p.push([a[u],t[u][l]]):3===n[l][u]&&f.push([a[u],t[u][l]]);v(e,m,"enterLong",!1,"green"),v(e,h,"enterLong",!0,"green"),v(e,f,"enterLong",!1,"red"),v(e,p,"enterLong",!0,"red");var y=[];for(l=0;l<r.length;l++)y.push({color:ne[l%ne.length],name:r[l],isLine:!0});y.push({color:"red",name:"Enter Short",hollow:!1}),y.push({color:"red",name:"Exit Short",hollow:!0}),y.push({color:"green",name:"Enter Long"}),y.push({color:"green",name:"Exit Long",hollow:!0}),F.createLegend(e,y,500,500)}()})),o.a.createElement("svg",{width:500+d+u,height:500+s+m},o.a.createElement("g",{ref:c,transform:"translate(".concat(d,",").concat(s,")")}))};!function(e){e[e.Short=1]="Short",e[e.Neutral=2]="Neutral",e[e.Long=3]="Long"}(n||(n={})),function(e){e[e.NoChange=-1]="NoChange",e[e.ExitLong=0]="ExitLong",e[e.EnterLong=1]="EnterLong",e[e.ExitShort=2]="ExitShort",e[e.EnterShort=3]="EnterShort"}(r||(r={}));var le=function(e){var t=e.data,a=0,i=[],c=[],s=["bollinger","williams_r","RSI","Random Forest","Buy and Hold"],u=[],m=[],d=0,h=[],f=Object(l.useState)(t.term[0]),p=Object(w.a)(f,2),g=p[0],E=p[1],b=Object(l.useState)(4),v=Object(w.a)(b,2),y=v[0],x=v[1],S=Object(l.useState)(2),k=Object(w.a)(S,2),j=k[0],_=k[1],L=Object(l.useState)(2),C=Object(w.a)(L,2),D=C[0],N=C[1],M=Object(l.useState)(-2),R=Object(w.a)(M,2),V=R[0],B=R[1],T=Object(l.useState)(50),A=Object(w.a)(T,2),P=A[0],F=A[1],z={};for(ne=0;ne<s.length;ne++)z[s[ne]]=!0;for(var $=Object(l.useState)(z),ee=Object(w.a)($,2),te=ee[0],ae=ee[1],ne=0;ne<t.dates.length;ne++)i.push(new Date(t.dates[ne])),c[ne]=[];Object.entries(t.strategy).forEach((function(e){var n=Object(w.a)(e,2),r=n[0],l=n[1];if(te[r]){for(ne=0;ne<l.cum_return.length;ne++)c[ne][a]=1e4*(1+l.cum_return[ne]);for(d=0,ne=0;ne<t.dates.length;ne++){if(!(new Date(t.dates[ne])>new Date(l.actions[d][0])))break;d++}m[a]=t.dates.map((function(e){return e===l.actions[d][0]?function(e){var t=0;return"enter"===e[1]&&(t+=1),"short"===e[2]&&(t+=2),t}(l.actions[d++]):-1})),u.push(r),a++}}));var le=n.Neutral,oe=r.NoChange,ie=1e4,ce=[];if(te.RSI){for(ne=0;ne<t.indicators.rel_strength.length;ne++){var se=t.indicators.rel_strength[ne];oe=r.NoChange,se>=P?(le===n.Short&&(oe=r.EnterLong),le=n.Long,ie*=1+t.daily_ret[ne]):(le===n.Long&&(oe=r.EnterShort),le=n.Short,ie*=1-t.daily_ret[ne]),c[ne][a]=ie,ce.push(oe)}m.push(ce),u.push("RSI at "+P),a++}var ue=0;le=n.Neutral,oe=r.NoChange,ie=1e4,ce=[];var me=function(e){return oe=r.EnterShort,ue=ie*(1-V/100),console.log("entered short",t.dates[e],"term: "+he),n.Short},de=function(e){return oe=r.EnterLong,ue=ie*(1+j/100),console.log("entered long",t.dates[e],"term: "+he),n.Long};if(te["Random Forest"]){for(u.push("Random Forest"),ne=0;ne<t.predict["term_"+g].predict.length;ne++){var he=t.predict["term_"+g].predict[ne];oe=r.NoChange,le===n.Long?ie>=ue&&(console.log("exit long",t.dates[ne],"term: "+he),he<=D?le=me(ne):(le=n.Neutral,oe=r.ExitLong)):le===n.Neutral?he>=y?le=de(ne):he<=D&&(le=me(ne)):ie>ue&&(console.log("exit short",t.dates[ne],"term: "+he),he>=y?le=de(ne):(le=n.Neutral,oe=r.ExitShort)),le===n.Long?ie*=1+t.daily_ret[ne]:le===n.Short&&(ie*=1-t.daily_ret[ne]),c[ne][a]=ie,ce.push(oe)}m.push(ce),a++}if(te["Buy and Hold"]){for(ie=1e4,ce=[],ne=0;ne<t.daily_ret.length;ne++)ie*=1+t.daily_ret[ne],c[ne][a]=ie,ce[ne]=-1;m.push(ce),u.push("Buy and Hold"),a++}var fe=function(e){ae(Object(I.a)({},te,Object(H.a)({},e.target.name,e.target.checked)))},pe=s.map((function(e){return o.a.createElement(X.a,{control:o.a.createElement(Z.a,{checked:te[e],onChange:fe,name:e}),label:e})}));h.push(o.a.createElement(O.a,{item:!0,lg:2,key:"strategies"},o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(W.a,null,o.a.createElement(Q.a,{component:"fieldset"},o.a.createElement(G.a,{component:"legend"},"Select Strategies to Show"),o.a.createElement(U.a,null,pe)))))),h.push(o.a.createElement(O.a,{item:!0,lg:4,key:1098},o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(re,{data:c,dates:i,trades:m,labels:u,title:"Strategy Returns for Initial Value $10000"}))));var ge=[],Ee=[];for(ne=0;ne<t.move.length;ne++)ge.push({value:ne+1,label:String(t.move[ne]+"%")}),Ee.push({value:ne,label:String(t.move[ne]+"%")});var be=[];for(ne=0;ne<t.term.length;ne++)be.push({value:t.term[ne],label:String(t.term[ne])});return h.push(o.a.createElement(O.a,{key:"randomForest",item:!0,lg:2},o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(q.a,{id:"discrete-slider-small-steps",gutterBottom:!0},o.a.createElement("b",null,"Random Forest Parameters",":")),o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(W.a,null,o.a.createElement(q.a,{id:"discrete-slider-small-steps",gutterBottom:!0},o.a.createElement("b",null,"Enter Long",":")),o.a.createElement("p",null,"Select cutoff percentage where strategy enters long position"),o.a.createElement(J.a,{name:"enterLong",defaultValue:4,step:1,marks:Ee,min:0,max:5,onChange:function(e,t){"number"==typeof t&&x(t)},valueLabelDisplay:"auto"}))),o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(W.a,null,o.a.createElement(q.a,{id:"discrete-slider-small-steps",gutterBottom:!0},o.a.createElement("b",null,"Exit Long",":")),o.a.createElement("p",null,"Select cutoff percentage where strategy exits long position"),o.a.createElement(J.a,{name:"exitLong",defaultValue:2,step:.01,marks:[],min:0,max:5,onChange:function(e,t){"number"==typeof t&&(console.log("long exit",t),_(t))},valueLabelDisplay:"auto"}))),o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(W.a,null,o.a.createElement(q.a,{id:"discrete-slider-small-steps",gutterBottom:!0},o.a.createElement("b",null,"Exit Short",":")),o.a.createElement("p",null,"Select cutoff percentage where strategy exits short position"),o.a.createElement(J.a,{name:"exitShort",defaultValue:-2,step:.01,marks:[],min:-5,max:0,onChange:function(e,t){"number"==typeof t&&B(t)},valueLabelDisplay:"auto"}))),o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(W.a,null,o.a.createElement(q.a,{id:"discrete-slider-small-steps",gutterBottom:!0},o.a.createElement("b",null,"Enter Short",":")),o.a.createElement("p",null,"Select cutoff percentage where strategy enters short position"),o.a.createElement(J.a,{name:"enterShort",defaultValue:2,marks:ge,min:1,max:6,onChange:function(e,t){"number"==typeof t&&N(t)},valueLabelDisplay:"auto"}))),o.a.createElement(K.a,{variant:"outlined"},o.a.createElement(W.a,null,o.a.createElement(q.a,{id:"discrete-slider-small-steps",gutterBottom:!0},o.a.createElement("b",null,"Enter prediction term",":")),o.a.createElement("p",null,"Select length of term that random forest trains on"),o.a.createElement(J.a,{defaultValue:5,step:null,marks:be,min:0,max:40,onChange:function(e,t){"number"==typeof t&&E(t)},valueLabelDisplay:"auto"})))))),h.push(o.a.createElement(Y,{onChange:function(e,t){"number"==typeof t&&F(t)},title:"RSI",description:"Select RSI value to go long/short",minVal:1,maxVal:99,defaultValue:50,labels:[]})),o.a.createElement("div",{className:"StartegiesLayout"},o.a.createElement(O.a,{container:!0,spacing:1},h))},oe=E((function(){var e=Object(l.useState)(!1),t=Object(w.a)(e,2),a=t[0],n=t[1],r=Object(l.useState)(""),i=Object(w.a)(r,2),c=i[0],s=i[1],u=Object(l.useState)(new Date),m=Object(w.a)(u,2),d=m[0],h=m[1],f=new Date;null===f||void 0===f||f.setMonth(f.getMonth()-3);var p=Object(l.useState)(f),g=Object(w.a)(p,2),E=g[0],b=g[1],v=Object(l.useState)(),y=Object(w.a)(v,2),x=y[0],S=y[1],R=V.a.create(),H=function(){var e=Object(j.a)(k.a.mark((function e(){var t,a,r,l;return k.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return n(!0),e.next=3,R.get("/api/analysis/example",{params:{symbol:c,start_date:B(E),end_date:B(d)}});case 3:if(t=e.sent,a=t.status,r=t.statusText,l=t.data,console.log(t),200!=a){e.next=11;break}S(l),n(!1),e.next=14;break;case 11:throw n(!1),console.log(a,r),new Error(r);case 14:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return o.a.createElement("div",{className:"StrategiesPage"},o.a.createElement("h1",null,"Strategies"),o.a.createElement("p",null,"This page is used to determine which strategies are useful in a model to predict stock direction. Please enter the Stock Ticker, the Start Date, End Date and then run!"),o.a.createElement(D.a,{utils:M.a},o.a.createElement(O.a,{container:!0,justify:"space-around"},o.a.createElement(_.a,{placeholder:"Enter Stock Ticker",inputProps:{"aria-label":"description"},onChange:function(e){return s(null===e||void 0===e?void 0:e.target.value)}}),o.a.createElement(N.a,{margin:"normal",id:"date-picker-dialog",label:"Start Date",format:"MM/dd/yyyy",value:E,onChange:b,KeyboardButtonProps:{"aria-label":"change date"}}),o.a.createElement(N.a,{margin:"normal",id:"date-picker-dialog",label:"End Date",format:"MM/dd/yyyy",value:d,onChange:h,KeyboardButtonProps:{"aria-label":"change date"}}),o.a.createElement(L.a,{variant:"contained",style:{justifySelf:"left"},onClick:function(){return H()},disabled:!c},"Run"))),a?o.a.createElement(C.a,{style:{alignContent:"center",height:"40px"}}):x&&o.a.createElement(le,{data:x}))})),ie=function(){return l.createElement(u.c,null,l.createElement(u.a,{exact:!0,path:"/",component:x}),l.createElement(u.a,{exact:!0,path:"/home",component:x}),l.createElement(u.a,{exact:!0,path:"/indicators",component:ae}),l.createElement(u.a,{exact:!0,path:"/strategies",component:oe}),l.createElement(u.a,{component:b}))},ce=a(23),se=Object(ce.a)(),ue=function(){return o.a.createElement(o.a.Fragment,null,o.a.createElement(s.Helmet,null,o.a.createElement("title",null,"Team TBD")),o.a.createElement(u.b,{history:se},o.a.createElement(ie,null)))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));c.a.render(o.a.createElement(ue,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[183,1,2]]]);
//# sourceMappingURL=main.447f9857.chunk.js.map