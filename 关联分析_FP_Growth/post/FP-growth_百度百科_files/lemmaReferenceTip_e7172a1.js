define("wiki-lemma:widget/lemma_content/mainContent/lemmaReference/lemmaReferenceTip/lemmaReferenceTip",function(e,t,i){function n(){a("span.ref.with-ctr").removeClass("with-ctr")}function r(e){a("span.ref[data-ctrid="+e+"]").addClass("with-ctr")}function f(e){for(var t=e.split(","),i=[],n=0;n<t.length;n++){var r=t[n],f=r.split(":");2===f.length&&i.push({ctrid:f[0],index:f[1]})}return i}var a=e("wiki-common:widget/lib/jquery/jquery"),s=e("wiki-common:widget/lib/jsmart/jsmart"),c=new s('{%foreach $refList as $ref%}\n<div class="J-reference-tip__item reference-tip__item reference-tip__item--type{%$ref.type|f_escape_xml%}" data-ctr="{%$ctrmap[$ref.index]|f_escape_xml%}">\n{%if $ref.type==1%}\n{%if ($refList|count)>1%}\n[{%$ref.index|f_escape_xml%}]&nbsp;{%/if%}\n{%$ref.title|f_escape_xml%}&nbsp;{%if $ref.site%}．{%$ref.site|f_escape_xml%}{%/if%}\n{%else if $ref.type==2%}\n{%if ($refList|count)>1%}\n[{%$ref.index|f_escape_xml%}]&nbsp;{%/if%}\n{%if $ref.author%}{%$ref.author|f_escape_xml%}{%/if%}\n{%if $ref.title%}．{%$ref.title|f_escape_xml%}{%/if%}\n{%if $ref.place%}．{%$ref.place|f_escape_xml%}{%/if%}\n{%if $ref.publisher%}：{%$ref.publisher|f_escape_xml%}{%/if%}\n{%if $ref.publishYear%}，{%$ref.publishYear|f_escape_xml%}{%/if%}\n{%else if $ref.type==3%}\n{%if ($refList|count)>1%}\n[{%$ref.index|f_escape_xml%}]&nbsp;{%/if%}\n{%$ref.text|f_escape_xml%}{%elseif $ref.type == "4"%}\n<div class="reference-tip__item--type4__content \n		{%if $ref.doubtStatus==1||$ref.doubtStatus==2%}\n			has-doubt\n		{%/if%}">\n{%if ($refList|count)>1%}\n[{%$ref.index|f_escape_xml%}]&nbsp;{%/if%}\n{%if $ref.name%}{%$ref.name|f_escape_xml%}．{%/if%}{%if $ref.typeName%}{%$ref.typeName|f_escape_xml%}．{%/if%}\n{%if $ref.isPublic > 0%}公开．{%else%}非公开．{%/if%}\n<span class="type4__remarks">\n由词条本人提供</span>\n{%if $ref.doubtStatus==1%}<span class="doubt-tag">已失效</span>\n{%/if%}\n{%if $ref.doubtStatus==2%}<span class="doubt-tag">有争议</span>\n{%/if%}\n</div>\n{%if $ref.isPublic > 0%}\n{%if $ref.imgs.length>0%}\n<div class=\'img-preview-container\'>\n{%foreach from=$ref.imgs item=img%}\n{%if $img.picUrl%}\n<a href="{%$img.picUrl|f_escape_xml%}" target="_blank">\n<div class="img-preview-container__img" style="background-image:url({%$img.picUrl|f_escape_xml%})"></div>\n</a>\n{%else%}\n<a href="{%\'http://imgsrc.baidu.com/baike/pic/item/\'|cat:$img.url|cat:\'.png\'%}" target="_blank">\n<div class="img-preview-container__img" style="background-image:url({%\'http://imgsrc.baidu.com/baike/pic/item/\'|cat:$img.url|cat:\'.png\'%})"></div>\n</a>\n{%/if%}\n{%/foreach%}\n</div>\n{%/if%}\n{%/if%}\n<a class="type4-detail-link" nslog-type="10090103" title="{%$ref.typeName|f_escape_xml%}" href="/personal/question/{%$lemmaTitle|f_escape_path%}/{%$subLemmaId|f_escape_path%}/{%$ref.id|f_escape_path%}" target="_blank">查看详情</a>\n{%/if%}\n</div>\n{%/foreach%}'),l=e("wiki-common:widget/component/nslog/nslog"),o=function(e){function t(){for(var t=!1,i=0;i<e.reference.length;i++){var n=e.reference[i];4===parseInt(n.type,10)&&(t=!0)}t&&l(10090101)}function i(t){for(var i=0;i<e.reference.length;i++){var n=e.reference[i];if(parseInt(n.index,10)===parseInt(t,10))return n}return null}var s=['<div class="reference-tip J-referenceTip">',"<table><tr>",'<td class="content"></td>','<td class="title" valign="middle">参考资料</td>',"</tr></table>",'<em class="triangle-bg"></em>','<em class="triangle-border"></em>',"</div>"].join(""),o=a(s),m=this,p=function(e){for(var t=e.toString().split("-"),i=parseInt(t[0],10),n=parseInt(t[t.length-1],10),r=[],f=i;n>=f;f++)r.push(f);return r};t();var u=null;this.display=function(t,n,a){var s=f(a);if(1===s.length&&s[0].ctrid&&r(s[0].ctrid),!u||!t.is(u)){u=t;for(var m=p(n),d=t.offset(),_=[],h=!1,$=0;$<m.length;$++){var g=i(m[$]);g&&(4===parseInt(g.type,10)&&(h=!0),_.push(g))}h&&l(10090102);var b={};s.forEach(function(e){b[e.index]=e.ctrid});var v=c.fetch({ctrmap:b,refList:_,subLemmaId:e.subLemmaId,lemmaTitle:e.lemmaTitle});o.find(".content").html(v),o.css({left:d.left-10,top:d.top+28}),this.show()}},this.show=function(){o.show()},this.hide=function(){u=null,o.hide()};var d=function(){var e=null;a(document.body).on("mouseover","sup",function(){a(this).hasClass("normal")||(e&&(clearTimeout(e),e=null),m.display(a(this),a(this).data("sup"),a(this).data("ctrmap")))}).on("mouseout","sup",function(){e&&(clearTimeout(e),e=null),e=setTimeout(function(){m.hide()},200),n()}).on("mouseover",".J-referenceTip",function(){e&&(clearTimeout(e),e=null)}).on("mouseout",".J-referenceTip",function(){e&&(clearTimeout(e),e=null),e=setTimeout(function(){m.hide()},200)}),a(document.body).on("mouseover",".J-reference-tip__item",function(){a(this).data("ctr")&&r(a(this).data("ctr"))}).on("mouseout",".J-reference-tip__item",function(){n()}),o.appendTo(a(document.body))};d()};i.exports=o});