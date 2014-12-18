<html>
<head>
<style type="text/css">
table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size: 9px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
}
table.gridtable th {
	border-width: 1px;
	padding: 1px;
	border-style: solid;
	border-color: #666666;
	background-color: #dedede;
}
table.gridtable td {
	border-width: 1px;
	padding: 1px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
}
</style>
</head>
<body>
<h1> Checklist heures</h1>
<%
   from operator import itemgetter, attrgetter
   toSort=[]
   for o in objects:
      toSort.append(( o.partner_id.name, o.account_id.name, o.line_id.name, o.date, o.time_beginning, o.time_end,o.time_quantity,o.line_id.to_invoice.name, o.line_id.to_invoice.factor, o.line_id.user_id.partner_id.name  ))
   endfor
   sortedList=sorted(toSort,key=itemgetter(0,1,3,4))
%>
<font face="verdana"size="1" >
<table class="gridtable" width="100%">
<tr>
<th>Client</th>
<th>Projet</th>
<th>Collaborateur</th> 
<th>Description du travail</th> 
<th  width="4%">Date</th> 
<th>Dét</th>
<th>Fin</th>
<th>Total</th>
<th>Facturable</th>
<th>Net</th>
</tr>
<%
old = ["","","","",""]
%>
%for t in sortedList:
<%
   if t[0] == old[0]:
      tmp0 = ""
   else :
      tmp0 =  t[0]
      old[0] = t[0]

   if t[1] == old[1]:
      tmp1 = ""
   else:
      tmp1= t[1]
      old[1]=t[1]
%>
<tr>
<td>${ tmp0 }</td>
<td>${ tmp1 }</td>
<td>${ t[9] }</td>
<td>${ t[2] }</td>
<td>${ t[3] }</td>
<td>${ t[4] }</td>
<td>${ t[5] }</td>
<td>${ t[6] }</td>
<td>${ t[7] }</td>
<td>${ t[6]-(t[8]*t[6]/100)  }</td>

</tr>
%endfor
</table>
</font>
</body>
</html>
