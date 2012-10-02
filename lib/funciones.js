var dirIP =  "corprocessu.com" // "localhost" //
var puerto = "8001"

var fotos;
var indiceFotos;

var minimoPrecio;
var maximoPrecio;
var minimoMetros;
var maximoMetros;

var fotosLista;
var imagenesLista;
var indiceLista;

var nro_reg = 5;
var pos_inicio = 0;

function inicioSesion(login, pass){
	jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_seg_users_0001_consulta_login",{"TK":"123456","login":login,"pswd":pass},function(resultado){
		if (resultado == "fracaso"){
			alert("Usuario no autorizado!");
		}
		else if (resultado == "inactivo"){
			alert("El usuario " + login + " se encuentra inactivo.");
		}
		else{
			//alert("Bienvenido " + login + "!")
			miRes0 = jQuery.parseJSON(resultado);
			//alert("Nombre completo: " + miRes0.name + " Propiedades registradas: " + miRes0.num_propias + " Propiedades compartidas: " + miRes0.num_compartidas + " Totales: " + miRes0.num_propiedades)
			localStorage.usr = login;
			location.href = "Menu.html";
		}
	})
}

function cerrarSesion(){
	localStorage.usr = "";
	location.href = "index.html"; 
}

function valorReg(tipo){
	document.getElementById('tipoReg').value=tipo;
}

function tipoReg(tipo){
	if(tipo==1)
		redireccionar('RegistroCorredor.html');
	else
		redireccionar('RegistroInmobiliaria.html');
}

function registrarCorredor(){
	var nombre = document.getElementById('nombre').value;
	var usr = document.getElementById('usr').value;
	var pass = document.getElementById('pass').value;
	var passC = document.getElementById('passC').value;
	var correo = document.getElementById('correo').value;
	var correoC = document.getElementById('correoC').value;
	var correoA = document.getElementById('correoA').value;
	var tlf1 = document.getElementById('tlf1').value;
	var tlf2 = document.getElementById('tlf2').value;
	var pagina_web = document.getElementById('pagWeb').value;
	
	var fecha_ingreso = obtiene_fecha();
	var active = "S";
	var priv_admin = "N";
	
	var  profesion = document.getElementById('selectProfesion').value;
	var  experiencia = document.getElementById('selectAnio').value;
	
	var nombres = ["Nombre Usuario", "Nombre y Apellido", "Correo", "Confirmar correo", "Contraseña", "Confirmar contraseña", "Telefono 1", "Profesión", "Año de Inicio laboral"];
	var parametros = [usr, nombre, correo, correoC, pass, passC, tlf1, profesion, experiencia];
	
	if (!parametrosVacios(parametros, nombres)){
		if(pass == passC){
			if(correo == correoC){
				//insertarcorredor
				//insertarUSR
				jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_seg_users_0001_inserta_usuario",{"TK":"123456","login":usr,"pswd":pass,"name":nombre,"email":correo,"active":active,"priv_admin":priv_admin,"email_alternativo":correoA,"fecha_ingreso":fecha_ingreso,"pagina_web":pagina_web},function(resultado){
					if(resultado == "exito"){
						alert('Usuario registrado con exito');
						redireccionar("index.html")
					}else if (resultado == "fracaso"){
						alert("El nombre de usuario ya está siendo utilizado");
						document.getElementById('nombre').value = "";
					}
				})				
				
			}else{
				alert('Los correos no coinciden');
				document.getElementById('correo').value = "";
				document.getElementById('correoC').value = "";
			}
		}else{
			alert('Las contraseñas no coinciden');
			document.getElementById('pass').value = "";
			document.getElementById('passC').value = "";
		}
	}
}

function parametrosVacios(parametros, nombres){
	vacios = new Array();
	resp = false;
	long=parametros.length;
	msj="OBLIGATORIAMENTE \nDebe llenar los campos:\n"
	
	for (var i=0; i < long; i++) {
		if(parametros[i] == ""){
			vacios.push(parametros[i]);
			msj += "\n - "+nombres[i];
		}
	}
	
	if (vacios.length != 0){
		resp = true;
		alert(msj);
	}
		
	return resp;
}

function listarProfesion(){
	acumulado = "<option value=''>Seleccionar</option>";
	jQuery.get("http://"+dirIP+":"+puerto+"/t_inm_profesiones_0001_consulta_profesiones",{"TK":"123456"},function(resultado){
		miRes = jQuery.parseJSON(resultado);
		$.each(miRes, function(i, elemento){
			acumulado += "<option id='"+elemento.profesion_sec+"' value='"+elemento.profesion_sec+"'>"+elemento.profesion_id+"</option>";
		})
		$("#selectProfesion").html(acumulado).selectmenu('refresh', true);
		listarAnio();
	})
}

function listarAnio(){
	acumulado = "<option value=''>Seleccionar</option>";
	var fecha=new Date();
	var anio=fecha.getFullYear();
	var i = anio;
	var lim = anio - 50
	
	while(i >= lim){
		acumulado += "<option id='"+i+"' value='"+(anio - i)+"'>"+i+"</option>";
		i--;
	}
	$("#selectAnio").html(acumulado).selectmenu('refresh', true);	
}

function agregarUsuario(login,pswd,name,email,priv_admin,email_alternativo,fecha_ingreso,pagina_web){
	var clave1 = document.getElementById('laClave1').value;
	var clave2 = document.getElementById('laClave2').value;
	if(clave1 == clave2){
		jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_seg_users_0001_inserta_usuario",{"TK":"123456","login":login,"pswd":pswd,"name":name,"email":email,"active":active,"priv_admin":priv_admin,"email_alternativo":email_alternativo,"fecha_ingreso":fecha_ingreso,"pagina_web":pagina_web},function(resultado){
			if(resultado == "exito"){
				location.href = "#page2";
			}
			else if (resultado == "fracaso"){
				location.href = "#page3";
			}
		})
		if(document.getElementById('optInmobiliaria').checked == true){
			$("form#logot").submit();
		}
	}
	else{
		alert('Las claves no coinciden');
		document.getElementById('laClave1').value = "";
		document.getElementById('laClave2').value = "";
	}
}

function obtiene_fecha(){
	var fecha_actual = new Date();
	var dia = fecha_actual.getDate();
	var mes = fecha_actual.getMonth() + 1;
	var anio = fecha_actual.getFullYear();
	var hora = fecha_actual.getHours();
	var minutos = fecha_actual.getMinutes();
	var segundos = fecha_actual.getSeconds();
	if (mes < 10){mes = '0' + mes}
	if (dia < 10){dia = '0' + dia}
	if (hora < 10){hora = '0' + hora}
	if (minutos < 10){minutos = '0' + minutos}
	if (segundos < 10){segundos = '0' + segundos}
	return (anio + "-" + mes + "-" + dia);
}

function listarEstados(){
	jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_crm_zona_niv2_0001_consulta_estados",{"TK":"123456","cor_zona_n1_sec":1},function(resultado){
		miRes1 = jQuery.parseJSON(resultado);
		acumulado1 = "<option id='ALL' value='ALL'>Todos los Estados</option>";
		$.each(miRes1, function(i, elemento){
			acumulado1 += "<option id='" + elemento.cor_zona_n2_sec + "' value='"+ elemento.cor_zona_n2_sec +"'>" + elemento.cor_zona_n2_id + "</option>";
		})
		$("#losEstados").html(acumulado1).selectmenu('refresh', true);
		listarCiudades(document.getElementById("losEstados").options[document.getElementById("losEstados").selectedIndex].id);
	})
}

function listarCiudades(estado){
	if(estado != "ALL"){
		jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_crm_zona_niv3_0001_consulta_ciudades",{"TK":"123456","cor_zona_n1_sec":1,"cor_zona_n2_sec":estado},function(resultado){
			miRes2 = jQuery.parseJSON(resultado);
			acumulado2 = "<option id='ALL' value='ALL'>Todas las Ciudades</option>";		
			$.each(miRes2, function(i, elemento){
				acumulado2 += "<option id=" + elemento.cor_zona_n3_sec + " value='" + elemento.cor_zona_n3_sec + "'>" + elemento.cor_zona_n3_id + "</option>";
			})
			$("#lasCiudades").empty();
			$("#lasCiudades").html(acumulado2).selectmenu('refresh', true);
			listarZonas(document.getElementById("losEstados").options[document.getElementById("losEstados").selectedIndex].id, document.getElementById("lasCiudades").options[document.getElementById("lasCiudades").selectedIndex].id);
		})
	}
	else{
		$("#lasCiudades").empty();
		$("#lasCiudades").html("<option id='ALL' value='ALL'>Todas las Ciudades</option>").selectmenu('refresh', true);
		$("#lasZonas").empty();
		$("#lasZonas").html("<option id='ALL' value='ALL'>Todas las Zonas</option>").selectmenu('refresh', true);
	}
}

function listarZonas(estado, ciudad){
	if(estado != "ALL"){
		if(ciudad != "ALL"){
			jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_crm_zona_niv4_0001_consulta_zonas",{"TK":"123456","cor_zona_n1_sec":1,"cor_zona_n2_sec":estado,"cor_zona_n3_sec":ciudad},function(resultado){
				miRes3 = jQuery.parseJSON(resultado);
				acumulado3 = "<option id='ALL' value='ALL'>Todas las Zonas</option>";
				$.each(miRes3, function(i, elemento){
					acumulado3 += "<option id=" + elemento.cor_zona_n4_sec + " value='" + elemento.cor_zona_n4_sec + "'>" + elemento.cor_zona_n4_id + "</option>"
				})
				$("#lasZonas").empty();
				$("#lasZonas").html(acumulado3).selectmenu('refresh', true);
			})
		}
		else{
			$("#lasZonas").empty();
			$("#lasZonas").html("<option id='ALL' value='ALL'>Todas las Zonas</option>").selectmenu('refresh', true);
		}
	}
	else{
		$("#lasZonas").empty();
		$("#lasZonas").html("<option id='ALL' value='ALL'>Todas las zonas</option>").selectmenu('refresh', true);
	}
}

function setPrecios(){
	jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_base_param_0002_consulta_parametro_rango_cantidad",{"TK":"123456","cor_paramsec":1},function(resultado){
		miRes4 = jQuery.parseJSON(resultado);
		$.each(miRes4, function(i, elemento){
			minimoPrecio = elemento.cor_param_cantidad1;
			maximoPrecio = elemento.cor_param_cantidad2;
			document.getElementById('minP').innerHTML = minimoPrecio;
			document.getElementById('maxP').innerHTML = maximoPrecio;
		})
	})
}

function actualizaPrecioMin(nivel){
	document.getElementById('minP').innerHTML = parseInt(minimoPrecio+((maximoPrecio-minimoPrecio)*(nivel/100)));
}

function actualizaPrecioMax(nivel){
	document.getElementById('maxP').innerHTML = parseInt(minimoPrecio+((maximoPrecio-minimoPrecio)*(nivel/100)));
}

function setMetros(){
	jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_base_param_0002_consulta_parametro_rango_cantidad",{"TK":"123456","cor_paramsec":2},function(resultado){
		miRes5 = jQuery.parseJSON(resultado);
		$.each(miRes5, function(i, elemento){
			minimoMetros = elemento.cor_param_cantidad1;
			maximoMetros = elemento.cor_param_cantidad2;
			document.getElementById('minM').innerHTML = minimoMetros;
			document.getElementById('maxM').innerHTML = maximoMetros;
		})
	})
}

function actualizaMetrosMin(nivel){
	document.getElementById('minM').innerHTML = parseInt(minimoMetros+((maximoMetros-minimoMetros)*(nivel/100)));
}

function actualizaMetrosMax(nivel){
	document.getElementById('maxM').innerHTML = parseInt(minimoMetros+((maximoMetros-minimoMetros)*(nivel/100)));
}

function listarHabBan(){
	jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_base_param_0002_consulta_parametro_rango_cantidad",{"TK":"123456","cor_paramsec":3},function(resultado){
		miRes6 = jQuery.parseJSON(resultado);
		$.each(miRes6, function(i, elemento){
			minimoHab = elemento.cor_param_cantidad1;
			maximoHab = elemento.cor_param_cantidad2;
			acumulado = "";
			var i;
			for(i = minimoHab; i <= maximoHab; i++){
				acumulado += "<option id='Hab"+i+"' value='Hab"+i+"'>"+i+"+</option>";
			}
			$("#Habitaciones").empty();
			$("#Habitaciones").html(acumulado).selectmenu('refresh', true);
		})
	})
	jQuery.get("http://"+dirIP+":"+puerto+"/t_cor_base_param_0002_consulta_parametro_rango_cantidad",{"TK":"123456","cor_paramsec":4},function(resultado){
		miRes7 = jQuery.parseJSON(resultado);
		$.each(miRes7, function(i, elemento){
			minimoBan = elemento.cor_param_cantidad1;
			maximoBan = elemento.cor_param_cantidad2;
			acumulado = "";
			var i;
			for(i = minimoBan; i <= maximoBan; i++){
				acumulado += "<option id='Ban"+i+"' value='Ban"+i+"'>"+i+"+</option>";
			}
			$("#Banos").empty();	
			$("#Banos").html(acumulado).selectmenu('refresh', true);
		})
	})
}

function listarTiposInm(){
	jQuery.get("http://"+dirIP+":"+puerto+"/t_inm_tipo_inmueble_0001_consulta_tipo_inmueble",{"TK":"123456"},function(resultado){
		miRes8 = jQuery.parseJSON(resultado);
		acumulado = "<option id='ALL' value='ALL'>Todas los Tipos</option>";
		$.each(miRes8, function(i, elemento){
			acumulado += "<option id=" + elemento.inm_tipoinmueble_sec + " value='" + elemento.inm_tipoinmueble_sec + "'>" + elemento.inm_tipoinmueble_id + "</option>";
		})
		$("#tipo_inm").html(acumulado).selectmenu('refresh', true);
	})
}

function buscar(modalidad, pais, estado, ciudad, zona, precioMin, precioMax, metrosMin, metrosMax, habitaciones, banos, tipo, codigo){
	location.href = "#page2";
	pos_inicio = 0;
	var codigoAlt = codigo
	if(codigo == ""){
		codigoAlt = "null"
	}
	fotosLista = null;
	imagenesLista = null;
	fotosLista = new Array();
	imagenesLista = new Array();
	indiceLista = 0;
	jQuery.get("http://"+dirIP+":"+puerto+"/t_inm_inmueble_0003_consulta_busqueda_inmueble_paginado",{"TK":"123456","inm_inmueble_operacion":modalidad,"cor_zona_n1_sec":pais, "cor_zona_n2_sec":estado,"cor_zona_n3_sec":ciudad,"cor_zona_n4_sec":zona,"precioMin":precioMin,"precioMax":precioMax, "metrosMin":metrosMin, "metrosMax":metrosMax, "habs":habitaciones, "banos":banos, "inm_tipoinmueble_sec":tipo,"inm_inmueble_sec":codigoAlt, "nro_reg":nro_reg, "pos_inicio":pos_inicio},function(resultado){
		miRes9 = jQuery.parseJSON(resultado);
		acumulado = "";
		$.each(miRes9,function(i, elemento){
		if(elemento.val!="123456"){
			codigo2 = elemento.inm_inmueble_sec;
			ciudad = elemento.ciudad;
			zona = elemento.zona;
			descripcion = elemento.inm_inmueble_desc;
			precio = elemento.inm_inmueble_precio;
			//canon = elemento.inm_inmueble_canon_bsf;
			metros = elemento.inm_inmueble_mtrsconstruccion;
			habitaciones = elemento.inm_inmueble_nro_hab;
			banos = elemento.inm_inmueble_nro_banos;
			operacion = elemento.inm_inmueble_operacion;
			operacion2 = "\'"+operacion+"\'"
			operacion3 = "";
			tipoInm = elemento.inm_tipoinmueble_sec;
			if(operacion == "V"){
				operacion3 = "Venta";
			}
			else if(operacion == "A"){
				operacion3 = "Alquiler";
			}
			elTipo = tipoInmueble(tipoInm);
			
			acumulado += "<li><a onclick=\"detalle("+codigo2+","+operacion2+");\" href='#page3'><img id='pic"+codigo2+"' src='http://" + dirIP + "/realtor_images/Casita.jpg' height='100' width='100'></img><h3>"+elTipo+" en "+operacion3+"</h3><p>COD #"+codigo2+"</p><p>"+ciudad+" / "+zona+"</p><p>"+descripcion+"</p><p>Bs. "+precio+"</p><p>"+metros+" mts<sup>2</sup></p><p>Habs: "+habitaciones+" / Baños: "+banos+"</p></a></li>";
			if (elemento.foto != "null"){
				fotosLista[indiceLista] = "http://" + dirIP + "/realtor_images/" + elemento.foto;
				imagenesLista[indiceLista] = "pic"+codigo2;
				indiceLista++;
			}
		}else{
			acumulado1 = "<li data-role='list-divider' role='heading' data-theme='a'><h3>Resultados coincidentes ("+elemento.cant+")</h3></li>";
			acumulado1 += acumulado;
			}
		})
		$("#espera").html("");
		$("#resultadosLista").html(acumulado1);
		$("#resultadosLista").listview('refresh');
		var i;
		for(i = 0; i < indiceLista; i++){
			document.images[imagenesLista[i]].src = fotosLista[i];
		}
	})
}

function buscarMas(modalidad, pais, estado, ciudad, zona, precioMin, precioMax, metrosMin, metrosMax, habitaciones, banos, tipo, codigo){
	location.href = "#page2";
	pos_inicio = pos_inicio + nro_reg; 
	
	modalidad = localStorage.modalidad;
	pais = 1;
	estado = document.getElementById('losEstados').value;
	ciudad = document.getElementById('lasCiudades').value;
	zona = document.getElementById('lasZonas').value;
	precioMin = minimoPrecio + ((maximoPrecio-minimoPrecio)*(document.getElementById('precio_min').value/100));
	precioMax = minimoPrecio + ((maximoPrecio-minimoPrecio)*(document.getElementById('precio_max').value/100)); 
	metrosMin = minimoMetros + ((maximoMetros-minimoMetros)*(document.getElementById('metros_min').value/100));
	metrosMax = minimoMetros + ((maximoMetros-minimoMetros)*(document.getElementById('metros_max').value/100));
	habitaciones = parseInt((document.getElementById('Habitaciones').options[document.getElementById('Habitaciones').selectedIndex].id).substring(3,4));
	banos = parseInt((document.getElementById('Banos').options[document.getElementById('Banos').selectedIndex].id).substring(3,4));
	tipo = document.getElementById('tipo_inm').value;
	codigo = document.getElementById('inm_sec').value
	
	var codigoAlt = codigo
	if(codigo == ""){
		codigoAlt = "null"
	}
	fotosLista = null;
	imagenesLista = null;
	fotosLista = new Array();
	imagenesLista = new Array();
	indiceLista = 0;
	jQuery.get("http://"+dirIP+":"+puerto+"/t_inm_inmueble_0003_consulta_busqueda_inmueble_paginado",{"TK":"123456","inm_inmueble_operacion":modalidad,"cor_zona_n1_sec":pais, "cor_zona_n2_sec":estado,"cor_zona_n3_sec":ciudad,"cor_zona_n4_sec":zona,"precioMin":precioMin,"precioMax":precioMax, "metrosMin":metrosMin, "metrosMax":metrosMax, "habs":habitaciones, "banos":banos, "inm_tipoinmueble_sec":tipo,"inm_inmueble_sec":codigoAlt, "nro_reg":nro_reg, "pos_inicio":pos_inicio},function(resultado){
		miRes9 = jQuery.parseJSON(resultado);
		acumulado = "";
		$.each(miRes9,function(i, elemento){
		if(elemento.val!="123456"){
			codigo2 = elemento.inm_inmueble_sec;
			ciudad = elemento.ciudad;
			zona = elemento.zona;
			descripcion = elemento.inm_inmueble_desc;
			precio = elemento.inm_inmueble_precio;
			//canon = elemento.inm_inmueble_canon_bsf;
			metros = elemento.inm_inmueble_mtrsconstruccion;
			habitaciones = elemento.inm_inmueble_nro_hab;
			banos = elemento.inm_inmueble_nro_banos;
			operacion = elemento.inm_inmueble_operacion;
			operacion2 = "\'"+operacion+"\'"
			operacion3 = "";
			tipoInm = elemento.inm_tipoinmueble_sec;
			if(operacion == "V"){
				operacion3 = "Venta";
			}
			else if(operacion == "A"){
				operacion3 = "Alquiler";
			}
			elTipo = tipoInmueble(tipoInm);
			
			acumulado += "<li><a onclick=\"detalle("+codigo2+","+operacion2+");\" href='#page3'><img id='pic"+codigo2+"' src='http://" + dirIP + "/realtor_images/Casita.jpg' height='100' width='100'></img><h3>"+elTipo+" en "+operacion3+"</h3><p>COD #"+codigo2+"</p><p>"+ciudad+" / "+zona+"</p><p>"+descripcion+"</p><p>Bs. "+precio+"</p><p>"+metros+" mts<sup>2</sup></p><p>Habs: "+habitaciones+" / Baños: "+banos+"</p></a></li>";
			if (elemento.foto != "null"){
				fotosLista[indiceLista] = "http://" + dirIP + "/realtor_images/" + elemento.foto;
				imagenesLista[indiceLista] = "pic"+codigo2;
				indiceLista++;
			}
		}
		})
		$("#resultadosLista").append(acumulado);
		$("#resultadosLista").listview('refresh');
		var i;
		for(i = 0; i < indiceLista; i++){
			document.images[imagenesLista[i]].src = fotosLista[i];
		}
	})
}

function tipoInmueble(tipoInm){
	if(tipoInm == "1"){
		elTipo = "Apartamento";
	}
	else if(tipoInm == "2"){
		elTipo = "Casa";
	}
	else if(tipoInm == "3"){
		elTipo = "Oficina";
	}
	else if(tipoInm == "4"){
		elTipo = "Galpón";
	}
	else if(tipoInm == "5"){
		elTipo = "Local";
	}
	else if(tipoInm == "6"){
		elTipo = "Terreno";
	}
	return elTipo;
}

function detalle(codigo, operacion){
	localStorage.cod = codigo;
	localStorage.op = operacion;
	jQuery.get("http://"+dirIP+":"+puerto+"/t_inm_inmueble_0002_consulta_busqueda_inmueble",{"TK":"123456","tipo_operacion":localStorage.op,"inm_inmueble_sec":localStorage.cod},function(resultado){
		miRes10 = jQuery.parseJSON(resultado);
		acumulado = "</br>";
		iniS = "<h3></h3><spam style=\"font-weight: normal;\">"
		finS = "</spam>"
		$.each(miRes10,function(i, elemento){			
			acumulado += "<li data-role='list-divider' role='heading'>"
			elTipo = tipoInmueble(elemento.inm_tipoinmueble_sec);
			acumulado += "<p><h3>"+elTipo+" en "+operacion3+"</h3></p>"
					
			if(elemento.inm_inmueble_canon_bsf=="N/A"){
				acumulado += "<p><h3>Precio: <spam style=\"font-weight: normal;\">"+elemento.inm_inmueble_precio+" BsF</spam></h3></p>"
			}else{
				acumulado += "<p><h3>Canon: <spam style=\"font-weight: normal;\">"+elemento.inm_inmueble_canon_bsf+"</spam></h3></p>"
			}
			acumulado += "</br><p>"+iniS+"<center>"+elemento.inm_inmueble_desc+"</center>"+finS+"</p>"
			
			acumulado += "</br><p><h3>Ubicación</h3></p>"
			acumulado += "<p>"+iniS+"Ciudad: "+elemento.ciudad+""+finS+"</p>"
			acumulado += "<p>"+iniS+"Zona: "+elemento.zona+""+finS+"</p>"
			
			acumulado += "</br><p><h3>Características</h3></p>"
			acumulado += "<p>"+iniS+"Habitaciones: "+elemento.inm_inmueble_nro_hab+""+finS+"</p>"
			acumulado += "<p>"+iniS+"Baños: "+elemento.inm_inmueble_nro_banos+""+finS+"</p>"
			acumulado += "<p>"+iniS+"Estacionamientos: "+elemento.inm_inmueble_nro_estac+""+finS+"</p>"
			acumulado += "<p>"+iniS+"Metros Cuadrados:"+elemento.inm_inmueble_mtrsconstruccion+""+finS+"</p>"
			
			acumulado += "</br><p><h3>Especificaciones</h3><spam style=\"font-weight: normal;\">"+elemento.inm_inmueble_especificaciones+"</spam></p>"
			
			jQuery.get("http://"+dirIP+":"+puerto+"/t_inm_corredor_0001_consulta_corredor",{"TK":"123456","login":elemento.inm_corredor},function(resultado){
			miRes12 = jQuery.parseJSON(resultado);
			$.each(miRes12,function(i, elemento){
		
				acumulado += "</br><p><h3>Corredor</h3></p>"
				acumulado += "<table><tr><td><img id='pic"+elemento.nombre+"' src='http://" + dirIP + "/realtor_images/corredores/"+elemento.inm_corredor_foto+" ' height='64' width='64'/></td>"
				acumulado += "<td><p>"+iniS+elemento.nombre+""+finS+"</p>"
				acumulado += "<p>"+iniS+"Correo: "+elemento.email+finS+"</p>"
				if(elemento.inm_corredor_telf1!="N/A" && elemento.inm_corredor_telf2!="N/A"){
					acumulado += "<p>"+iniS+"Teléfonos: "+elemento.inm_corredor_telf1+" / "+elemento.inm_corredor_telf2+finS+"</p>"
				}else if(elemento.inm_corredor_telf1=="N/A" && elemento.inm_corredor_telf2!="N/A"){
					acumulado += "<p>"+iniS+"Teléfono: "+elemento.inm_corredor_telf2+finS+"</p>"
				}else if(elemento.inm_corredor_telf1!="N/A" && elemento.inm_corredor_telf2=="N/A"){					
					acumulado += "<p>"+iniS+"Teléfono: "+elemento.inm_corredor_telf1+finS+"</p>"
				}				
				acumulado += "</td></tr></table></li>"
				
				})

				jQuery.get("http://"+dirIP+":"+puerto+"/t_inm_inmueble_fotos_0001_consulta_fotos",{"TK":"123456","inm_inmueble_sec":localStorage.cod},function(resultado){
					miRes11 = jQuery.parseJSON(resultado);
					fotos = null;
					fotos = new Array();
					indiceFotos = 0;
					$.each(miRes11,function(i, elemento){
						fotos[i] = elemento.inm_inmueblefoto_ruta_nombre;
					})
					if(fotos.length>0){
						laImagen = new Image();
						laImagen.src = "http://" + dirIP + "/realtor_images/" + fotos[0];
						document.images["fotoInmueble"].src = laImagen.src;
						document.images["fotoInmueble"].width = (200 * laImagen.width) / laImagen.height;
						document.images["fotoInmueble"].height = 200;
					}
					else{
						document.images["fotoInmueble"].src = "http://" + dirIP + "/realtor_images/Casita.jpg";
						document.images["fotoInmueble"].width = 200;
						document.images["fotoInmueble"].height = 200;
					}
					$("#espera2").html("");
					$("#resultadosLista2").html(acumulado);
					$("#resultadosLista2:visible").listview('refresh',true);
					//document.getElementById('datosDetalle').innerHTML = acumulado;
					document.getElementById('losBotones').style.visibility = 'visible';
				})
			})
		})
	})
}

function anteriorFoto(){
	if(fotos.length > 0){
		if (indiceFotos > 0){
			indiceFotos--;
		}
		else{
			indiceFotos = (fotos.length - 1);
		}
		laImagen = new Image();
		laImagen.src = "http://" + dirIP + "/realtor_images/" + fotos[indiceFotos];
		document.images["fotoInmueble"].src = laImagen.src;
		document.images["fotoInmueble"].width = (200 * laImagen.width) / laImagen.height;
		document.images["fotoInmueble"].height = 200;
	}
}

function siguienteFoto(){
	if(fotos.length > 0){
		if (indiceFotos < fotos.length - 1){
			indiceFotos++;
		}
		else{
			indiceFotos = 0;
		}
		laImagen = new Image();
		laImagen.src = "http://" + dirIP + "/realtor_images/" + fotos[indiceFotos];
		document.images["fotoInmueble"].src = laImagen.src;
		document.images["fotoInmueble"].width = (200 * laImagen.width) / laImagen.height;
		document.images["fotoInmueble"].height = 200;
	}
}

function redireccionar(url) {
	localStorage.regresar = url;
	window.open(url,"_self");
}