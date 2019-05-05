<%inherit file="base.mako" />


<%block name="content">
<link rel="stylesheet" href="${request.static_url('deform:static/css/bootstrap.min.css')}" type="text/css" media="screen" charset="utf-8"/>
<link rel="stylesheet" href="${request.static_url('deform:static/css/form.css')}" type="text/css"/>
%for reqt in view.reqts['css']:
    <link rel="stylesheet" type="text/css" href="${request.static_url(reqt)}"/>
%endfor
<script src="${request.static_url('deform:static/scripts/jquery-2.0.3.min.js')}" type="text/javascript"></script>
<script src="${request.static_url('deform:static/scripts/bootstrap.min.js')}" type="text/javascript"></script>
%for reqt in view.reqts['js']:
    <script src="${request.static_url(reqt)}" type="text/javascript"></script>
%endfor

<h2>${heading}</h2>
<div style="width: 33%">
<p>${form | n}</p>
</div>
<script type="text/javascript">
    deform.load()
</script>
</%block>
