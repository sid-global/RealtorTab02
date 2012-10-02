from bottle import hook, response, route, run, static_file, request, redirect, post
import sqlite3
import psycopg2
import json
import socket
import ast
import time
import decimal
import datetime

tokenSistema = "123456"

# Servidor Local Venezuela
directorio = "C:/Ale/"
confBaseDatos = "dbname=realtor_tab user=postgres password=root host=sid_db_02"

# Servidor Remoto Canada
# directorio = "C:/SID/En proceso/Realtor_tab/bottlepy"
# confBaseDatos = "dbname=realtor_tab user=postgres password=Master1029"

# OJO: esta funcion evita que ocurran errores de tipo 'Access-Control-Allow-Origin'
# referidos a la conexion. Si estos errores ocurren ya son por otras razones.
@hook('after_request')
def enable_cors():
	response.headers['Access-Control-Allow-Origin'] = '*'

# Protocolo general: para acceder a cualquiera de estos servicios, el primer
# parametro enviado por GET debe ser el 'Token de Sistema', el cual se define 
# como una variable global. Esto evita que personas ajenas alteren la base de 
# datos desde la barra de direcciones de un navegador.

# *** Funcion maestra para consultas ***
# TK tiene el string con el token de sistema enviada por el cliente
# consulta tiene el string SQL que se ejecutara en la BD
# campos es una lista con los strings de los nombres de los campos que se van a obtener
# params es una lista con los strings de los parametros de los que depende la consulta SQL
def consultas(TK, consulta, campos, params, modo):
	if TK == tokenSistema:
		conexion = psycopg2.connect(confBaseDatos)
		miCursor = conexion.cursor()
		nParams = len(params)
		if nParams == 0:
			try:
				miCursor.execute(consulta)
			except psycopg2.IntegrityError:
				return "fracaso"
		elif nParams > 0:
			try:
				miCursor.execute(consulta,tuple(params))
			except psycopg2.IntegrityError:
				return "fracaso"
		if modo == "consulta":
			losDatos = miCursor.fetchall()
			resultado = []
			nCampos = len(campos)
			for tupla in losDatos:
				i = 0
				elDicc = "{"
				while i < nCampos:
					if isinstance(tupla[i], int) or isinstance(tupla[i], long) or isinstance(tupla[i], decimal.Decimal):
						elDicc += "'" + campos[i] + "':" + str(tupla[i]) + ","
					elif isinstance(tupla[i], str) or isinstance(tupla[i], datetime.datetime):
						elDicc += "'" + campos[i] + "':'" + unicode(str(tupla[i]), "utf-8") + "',"
					else:
						elDicc += "'" + campos[i] + "':'" + unicode("N/A", "utf-8") + "',"
					i+=1
				elDicc = elDicc[:len(elDicc)-1]
				elDicc += "}"
				try:
					print "\n" + elDicc + "\n"
				except UnicodeEncodeError:
					print "\nError de Unicode\n"
				resultado.append(ast.literal_eval(elDicc))
			return json.dumps(resultado, ensure_ascii=False)
		elif modo == "inserta" or modo == "elimina":
			conexion.commit()
			return "exito"
		conexion.close()
	else:
		return ""
		
@route('/t_inm_tipo_inmueble_0001_consulta_tipo_inmueble')
def t_inm_tipo_inmueble_0001_consulta_tipo_inmueble():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select inm_tipoinmueble_sec, inm_tipoinmueble_id from inm_tipo_inmueble where inm_tipoinmueble_activo = 'S'"
	campos = ["inm_tipoinmueble_sec", "inm_tipoinmueble_id"]
	parametros = []
	return consultas(TK, query, campos, parametros,"consulta")

@route('/t_cor_crm_zona_niv2_0001_consulta_estados')
def t_cor_crm_zona_niv2_0001_consulta_estados():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select cor_zona_n2_sec, cor_zona_n2_id from cor_crm_zona_niv2 where cor_zona_n1_sec = %s and cor_zona_n2_activo = 'S' order by cor_zona_n2_id"
	campos = ["cor_zona_n2_sec", "cor_zona_n2_id"]
	parametros = [recibido["cor_zona_n1_sec"]]
	return consultas(TK, query, campos, parametros, "consulta")

@route('/t_cor_crm_zona_niv3_0001_consulta_ciudades')
def t_cor_crm_zona_niv3_0001_consulta_ciudades():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select cor_zona_n3_sec, cor_zona_n3_id from cor_crm_zona_niv3 where cor_zona_n1_sec = %s and cor_zona_n2_sec = %s and cor_zona_n3_activo = 'S' order by cor_zona_n3_id"
	campos = ["cor_zona_n3_sec", "cor_zona_n3_id"]
	parametros = [recibido["cor_zona_n1_sec"], recibido["cor_zona_n2_sec"]]
	return consultas(TK, query, campos, parametros, "consulta")

@route('/t_cor_crm_zona_niv4_0001_consulta_zonas')
def t_cor_crm_zona_niv4_0001_consulta_zonas():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select cor_zona_n4_sec, cor_zona_n4_id, cor_zona_n4_cod_postal from cor_crm_zona_niv4 where cor_zona_n1_sec = %s and cor_zona_n2_sec = %s and cor_zona_n3_sec = %s and cor_zona_n4_activo = 'S' order by cor_zona_n4_id"
	campos = ["cor_zona_n4_sec", "cor_zona_n4_id", "cor_zona_n4_cod_postal"]
	parametros = [recibido["cor_zona_n1_sec"],recibido["cor_zona_n2_sec"],recibido["cor_zona_n3_sec"]]
	return consultas(TK, query, campos, parametros, "consulta")
	
@route('/t_cor_base_param_0001_consulta_parametro_cantidad')
def t_cor_base_param_0001_consulta_parametro_cantidad():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select cor_param_cantidad1 from cor_base_param where cor_paramsec = %s and cor_param_activo = 'S'"
	campos = ["cor_param_cantidad1"]
	parametros = [recibido["cor_paramsec"]]
	return consultas(TK, query, campos, parametros, "consulta")

@route('/t_cor_base_param_0002_consulta_parametro_rango_cantidad')
def t_cor_base_param_0002_consulta_parametro_rango_cantidad():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select cor_param_cantidad1, cor_param_cantidad2 from cor_base_param where cor_paramsec = %s and cor_param_activo = 'S'"
	campos = ["cor_param_cantidad1","cor_param_cantidad2"]
	parametros = [recibido["cor_paramsec"]]
	return consultas(TK, query, campos, parametros,"consulta")

@route('/t_cor_seg_users_0001_consulta_login')
def t_cor_seg_users_0001_consulta_login():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select name, active from cor_seg_users where login = %s and pswd = %s"
	campos = ["name","active"]
	parametros = [recibido["login"],recibido["pswd"]]
	resultado = eval(consultas(TK, query, campos, parametros,"consulta")+"")
	if resultado != "":
		if len(resultado) == 1:
			if resultado[0]["active"] == "S":
				
				query2 = "select count(inm_inmueble_sec) as total from inm_inmueble where inm_corredor = %s"
				campos2 = ["total"]
				parametros2 = [recibido["login"]]
				total = eval(consultas(TK, query2, campos2, parametros2, "consulta")+"")
				
				query3 = "select count(inm_inmueble_sec) as total from inm_inmueble where inm_inmueble_compartida = 'G' and inm_inmueble_sec in (select inm_inmueble_sec from inm_inmueble_gvt where inm_gvt_sec in (select inm_gvt_sec from inm_gvt where inm_gvt_id in (select inm_gvt_id from inm_gvt_detalle where login = %s)))"
				campos3 = ["total"]
				parametros3 = [recibido["login"]]
				total2 = eval(consultas(TK, query3, campos3, parametros3, "consulta")+"")
				
				query4 = "SELECT COUNT(inm_gvt_sec) FROM inm_gvt WHERE inm_gvt_propietario = %s"
				campos4 = ["total"]
				parametros4 = [recibido["login"]]
				total3 = eval(consultas(TK, query4, campos4, parametros4, "consulta")+"")
				
				N_propiedades_personales = total[0]["total"]
				N_propiedades_compartidas = total2[0]["total"]
				N_propiedades_totales = N_propiedades_personales + N_propiedades_compartidas
				N_grupos_virtuales = total3[0]["total"]
				
				return json.dumps({"name":resultado[0]["name"],"num_propiedades": N_propiedades_totales,"num_propias":N_propiedades_personales,"num_compartidas":N_propiedades_compartidas,"num_gv":N_grupos_virtuales})
			else:
				return "inactivo"
		else:
			return "fracaso"

@route('/t_cor_seg_session_0001_inserta_usuario_logueado')
def t_cor_seg_session_0001_inserta_usuario_logueado():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "insert into cor_seg_session values(%s,%s,%s)"
	campos = []
	tiempo = time.localtime()
	ano = str(tiempo[0])
	mes = str(tiempo[1])
	dia = str(tiempo[2])
	hora = str(tiempo[3])
	minutos = str(tiempo[4])
	segundos = str(tiempo[5])
	conexion = psycopg2.connect(confBaseDatos)
	miCursor = conexion.cursor()
	miCursor.execute("select nextval('cor_seg_session_sec')")
	losDatos = miCursor.fetchall()
	parametros = [losDatos[0][0],recibido["login"],ano+"-"+mes+"-"+dia+" "+hora+":"+minutos+":"+segundos+"-4:30"]
	return consultas(TK, query, campos, parametros,"inserta")

@route('/t_cor_seg_session_0002_elimina_usuario_logueado')
def t_cor_seg_session_0002_elimina_usuario_logueado():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "delete from cor_seg_session where cor_session_sec = %s"
	campos = []
	parametros = [recibido["secuencia"]]
	return consultas(TK, query, campos, parametros, "elimina")

@route('/t_inm_inmueble_0001_consulta_busqueda_inmueble')
def t_inm_inmueble_0001_consulta_busqueda_inmueble():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	pedazosQuery = []
	parametros = []	
	query = """select inm.inm_inmueble_sec, inm.inm_inmueble_desc, inm.inm_inmueble_operacion, inm.inm_tipoinmueble_sec,
	inm.inm_inmueble_precio,inm.inm_inmueble_canon_bsf, inm.inm_inmueble_mtrsconstruccion, inm.inm_inmueble_nro_hab,
	inm.inm_inmueble_nro_banos,	pais.cor_zona_n1_id, estado.cor_zona_n2_id, ciudad.cor_zona_n3_id, zona.cor_zona_n4_id from
	cor_crm_zona_niv1 as pais inner join cor_crm_zona_niv2 as estado on pais.cor_zona_n1_sec = estado.cor_zona_n1_sec inner join
	cor_crm_zona_niv3 as ciudad on ciudad.cor_zona_n1_sec = estado.cor_zona_n1_sec and ciudad.cor_zona_n2_sec = estado.cor_zona_n2_sec
	inner join cor_crm_zona_niv4 as zona on zona.cor_zona_n1_sec = ciudad.cor_zona_n1_sec and zona.cor_zona_n2_sec = ciudad.cor_zona_n2_sec
	and zona.cor_zona_n3_sec = ciudad.cor_zona_n3_sec inner join inm_inmueble as inm on inm.cor_zona_n1_sec = pais.cor_zona_n1_sec 
	and inm.cor_zona_n2_sec = estado.cor_zona_n2_sec and inm.cor_zona_n3_sec = ciudad.cor_zona_n3_sec and
	inm.cor_zona_n4_sec = zona.cor_zona_n4_sec where inm.inm_inmueble_estatus = 'P'"""
	
	if recibido["inm_inmueble_sec"] != "null":
		pedazosQuery.append(" inm.inm_inmueble_sec = %s")
		parametros.append(recibido["inm_inmueble_sec"])
	else:
		if recibido["inm_inmueble_operacion"] != "T":
			pedazosQuery.append(" inm.inm_inmueble_operacion = %s")
			parametros.append(recibido["inm_inmueble_operacion"])
		if recibido["cor_zona_n1_sec"] != "ALL":
			pedazosQuery.append(" inm.cor_zona_n1_sec = %s")
			parametros.append(recibido["cor_zona_n1_sec"])
		if recibido["cor_zona_n2_sec"] != "ALL":
			pedazosQuery.append(" inm.cor_zona_n2_sec = %s")
			parametros.append(recibido["cor_zona_n2_sec"])
		if recibido["cor_zona_n3_sec"] != "ALL":
			pedazosQuery.append(" inm.cor_zona_n3_sec = %s")
			parametros.append(recibido["cor_zona_n3_sec"])
		if recibido["cor_zona_n4_sec"] != "ALL":
			pedazosQuery.append(" inm.cor_zona_n4_sec = %s")
			parametros.append(recibido["cor_zona_n4_sec"])
		if recibido["inm_tipoinmueble_sec"]  != "ALL":
			pedazosQuery.append(" inm.inm_tipoinmueble_sec = %s")
			parametros.append(recibido["inm_tipoinmueble_sec"])
		query += " and inm_inmueble_precio between " + recibido["precioMin"] + " and " + recibido["precioMax"]
		query += " and inm_inmueble_mtrsconstruccion between " + recibido["metrosMin"] + " and " + recibido["metrosMax"]
		query += " and inm_inmueble_nro_hab >= " + recibido["habs"]
		query += " and inm_inmueble_nro_banos >= " + recibido["banos"]
	for pedazo in pedazosQuery:
		query += " and" + pedazo
	print query
	campos = ["inm_inmueble_sec", "inm_inmueble_desc", "inm_inmueble_operacion", "inm_tipoinmueble_sec", "inm_inmueble_precio", "inm_inmueble_canon_bsf",  "inm_inmueble_mtrsconstruccion", "inm_inmueble_nro_hab", "inm_inmueble_nro_banos", "pais", "estado", "ciudad", "zona"]	
	losDatosInmueble = eval(consultas(TK, query, campos, parametros, "consulta")+"")
	for elInmueble in losDatosInmueble:
		query2 = "select inm_inmueblefoto_ruta_nombre from inm_inmueble_fotos where inm_inmueble_sec = %s"
		campos2 = ["inm_inmueblefoto_ruta_nombre"]
		parametros2 = [elInmueble["inm_inmueble_sec"]]
		datosFotos = eval(consultas(TK, query2, campos2, parametros2, "consulta")+"")
		laFoto = "null"
		if len(datosFotos) > 0:
			laFoto = datosFotos[0]["inm_inmueblefoto_ruta_nombre"]
		elInmueble.update({"foto":laFoto})
		print "\n" + str(elInmueble) + "\n"
	return json.dumps(losDatosInmueble)
	
@route('/t_inm_inmueble_0002_consulta_busqueda_inmueble')
def t_inm_inmueble_0002_consulta_busqueda_inmueble():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = ""
	if recibido["tipo_operacion"] == "V":	
		query = """select inm.*, pais.cor_zona_n1_id, estado.cor_zona_n2_id, ciudad.cor_zona_n3_id, zona.cor_zona_n4_id from cor_crm_zona_niv1 
		as pais inner join cor_crm_zona_niv2 as estado on pais.cor_zona_n1_sec = estado.cor_zona_n1_sec inner join cor_crm_zona_niv3 as ciudad
		on ciudad.cor_zona_n1_sec = estado.cor_zona_n1_sec and ciudad.cor_zona_n2_sec = estado.cor_zona_n2_sec inner join 
		cor_crm_zona_niv4 as zona on zona.cor_zona_n1_sec = ciudad.cor_zona_n1_sec and zona.cor_zona_n2_sec = ciudad.cor_zona_n2_sec and
		zona.cor_zona_n3_sec = ciudad.cor_zona_n3_sec inner join inm_inmueble as inm on inm.cor_zona_n1_sec = pais.cor_zona_n1_sec 
		and inm.cor_zona_n2_sec = estado.cor_zona_n2_sec and inm.cor_zona_n3_sec = ciudad.cor_zona_n3_sec and
		inm.cor_zona_n4_sec = zona.cor_zona_n4_sec where inm.inm_inmueble_estatus = 'P' and inm.inm_inmueble_sec = %s and inm.inm_inmueble_operacion = 'V'"""
	elif recibido["tipo_operacion"] == "A":
		query = """select inm.*, pais.cor_zona_n1_id, estado.cor_zona_n2_id, ciudad.cor_zona_n3_id, zona.cor_zona_n4_id from cor_crm_zona_niv1 
		as pais inner join cor_crm_zona_niv2 as estado on pais.cor_zona_n1_sec = estado.cor_zona_n1_sec inner join cor_crm_zona_niv3 as ciudad
		on ciudad.cor_zona_n1_sec = estado.cor_zona_n1_sec and ciudad.cor_zona_n2_sec = estado.cor_zona_n2_sec inner join 
		cor_crm_zona_niv4 as zona on zona.cor_zona_n1_sec = ciudad.cor_zona_n1_sec and zona.cor_zona_n2_sec = ciudad.cor_zona_n2_sec and
		zona.cor_zona_n3_sec = ciudad.cor_zona_n3_sec inner join inm_inmueble as inm on inm.cor_zona_n1_sec = pais.cor_zona_n1_sec 
		and inm.cor_zona_n2_sec = estado.cor_zona_n2_sec and inm.cor_zona_n3_sec = ciudad.cor_zona_n3_sec and
		inm.cor_zona_n4_sec = zona.cor_zona_n4_sec where inm.inm_inmueble_estatus = 'P' and inm.inm_inmueble_sec = %s and inm.inm_inmueble_operacion = 'A'"""
	elif recibido["tipo_operacion"] == "T":
		query = """select inm.*, pais.cor_zona_n1_id, estado.cor_zona_n2_id, ciudad.cor_zona_n3_id, zona.cor_zona_n4_id from cor_crm_zona_niv1 
		as pais inner join cor_crm_zona_niv2 as estado on pais.cor_zona_n1_sec = estado.cor_zona_n1_sec inner join cor_crm_zona_niv3 as ciudad
		on ciudad.cor_zona_n1_sec = estado.cor_zona_n1_sec and ciudad.cor_zona_n2_sec = estado.cor_zona_n2_sec inner join 
		cor_crm_zona_niv4 as zona on zona.cor_zona_n1_sec = ciudad.cor_zona_n1_sec and zona.cor_zona_n2_sec = ciudad.cor_zona_n2_sec and
		zona.cor_zona_n3_sec = ciudad.cor_zona_n3_sec inner join inm_inmueble as inm on inm.cor_zona_n1_sec = pais.cor_zona_n1_sec 
		and inm.cor_zona_n2_sec = estado.cor_zona_n2_sec and inm.cor_zona_n3_sec = ciudad.cor_zona_n3_sec and
		inm.cor_zona_n4_sec = zona.cor_zona_n4_sec where inm.inm_inmueble_estatus = 'P' and inm.inm_inmueble_sec = %s"""
	campos = ["inm_inmueble_sec", "inm_inmueble_desc", "inm_inmueble_operacion", "inm_tipoinmueble_sec", "cor_zona_n1_sec", "cor_zona_n2_sec", "cor_zona_n3_sec", "cor_zona_n4_sec", "inm_inmueble_zona_detalle", "inm_inmueble_nombre_res", "inm_inmueble_piso", "inm_inmueble_apto", "inm_inmueble_precio", "inm_inmueble_canon_bsf", "inm_inmueble_ppto_maximo", "inm_inmueble_precio_mercado", "inm_inmueble_mtrsconstruccion", "inm_inmueble_mtrsterreno", "inm_inmueble_nro_hab", "inm_inmueble_nro_banos", "inm_inmueble_nro_estac", "inm_inmueble_fec_construccion", "inm_inmueble_especificaciones", "inm_corredor", "inm_propietario_nombre", "inm_propietario_telf", "inm_propietario_cel", "inm_propietario_email", "inm_propietario_comision", "inm_inmueble_compartida", "inm_inmueble_fec_mod", "inm_inmueble_ip_mod", "inm_inmueble_login_mod", "inm_inmueble_estatus", "inm_inmueble_fec_registro", "inm_inmueble_nro_visitas", "inm_inmueble_nro_oficinas", "inm_inmueble_nro_pisos", "inm_inmueble_area_neta", "inm_inmueble_proc_constr", "pais", "estado", "ciudad", "zona"]
	parametros = [recibido["inm_inmueble_sec"]]
	return consultas(TK, query, campos, parametros, "consulta")
	
@route('/t_inm_inmueble_0003_consulta_busqueda_inmueble_paginado')
def t_inm_inmueble_0003_consulta_busqueda_inmueble_paginado():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	pedazosQuery = []
	parametros = []	
	query = """select inm.inm_inmueble_sec, inm.inm_inmueble_desc, inm.inm_inmueble_operacion, inm.inm_tipoinmueble_sec,
	inm.inm_inmueble_precio,inm.inm_inmueble_canon_bsf, inm.inm_inmueble_mtrsconstruccion, inm.inm_inmueble_nro_hab,
	inm.inm_inmueble_nro_banos,	pais.cor_zona_n1_id, estado.cor_zona_n2_id, ciudad.cor_zona_n3_id, zona.cor_zona_n4_id from
	cor_crm_zona_niv1 as pais inner join cor_crm_zona_niv2 as estado on pais.cor_zona_n1_sec = estado.cor_zona_n1_sec inner join
	cor_crm_zona_niv3 as ciudad on ciudad.cor_zona_n1_sec = estado.cor_zona_n1_sec and ciudad.cor_zona_n2_sec = estado.cor_zona_n2_sec
	inner join cor_crm_zona_niv4 as zona on zona.cor_zona_n1_sec = ciudad.cor_zona_n1_sec and zona.cor_zona_n2_sec = ciudad.cor_zona_n2_sec
	and zona.cor_zona_n3_sec = ciudad.cor_zona_n3_sec inner join inm_inmueble as inm on inm.cor_zona_n1_sec = pais.cor_zona_n1_sec 
	and inm.cor_zona_n2_sec = estado.cor_zona_n2_sec and inm.cor_zona_n3_sec = ciudad.cor_zona_n3_sec and
	inm.cor_zona_n4_sec = zona.cor_zona_n4_sec where inm.inm_inmueble_estatus = 'P'"""
	
	query0 = """select count(*) from
	cor_crm_zona_niv1 as pais inner join cor_crm_zona_niv2 as estado on pais.cor_zona_n1_sec = estado.cor_zona_n1_sec inner join
	cor_crm_zona_niv3 as ciudad on ciudad.cor_zona_n1_sec = estado.cor_zona_n1_sec and ciudad.cor_zona_n2_sec = estado.cor_zona_n2_sec
	inner join cor_crm_zona_niv4 as zona on zona.cor_zona_n1_sec = ciudad.cor_zona_n1_sec and zona.cor_zona_n2_sec = ciudad.cor_zona_n2_sec
	and zona.cor_zona_n3_sec = ciudad.cor_zona_n3_sec inner join inm_inmueble as inm on inm.cor_zona_n1_sec = pais.cor_zona_n1_sec 
	and inm.cor_zona_n2_sec = estado.cor_zona_n2_sec and inm.cor_zona_n3_sec = ciudad.cor_zona_n3_sec and
	inm.cor_zona_n4_sec = zona.cor_zona_n4_sec where inm.inm_inmueble_estatus = 'P'"""
	
	if recibido["inm_inmueble_sec"] != "null":
		pedazosQuery.append(" inm.inm_inmueble_sec = %s")
		parametros.append(recibido["inm_inmueble_sec"])
	else:
		if recibido["inm_inmueble_operacion"] != "T":
			pedazosQuery.append(" inm.inm_inmueble_operacion = %s")
			parametros.append(recibido["inm_inmueble_operacion"])
		if recibido["cor_zona_n1_sec"] != "ALL":
			pedazosQuery.append(" inm.cor_zona_n1_sec = %s")
			parametros.append(recibido["cor_zona_n1_sec"])
		if recibido["cor_zona_n2_sec"] != "ALL":
			pedazosQuery.append(" inm.cor_zona_n2_sec = %s")
			parametros.append(recibido["cor_zona_n2_sec"])
		if recibido["cor_zona_n3_sec"] != "ALL":
			pedazosQuery.append(" inm.cor_zona_n3_sec = %s")
			parametros.append(recibido["cor_zona_n3_sec"])
		if recibido["cor_zona_n4_sec"] != "ALL":
			pedazosQuery.append(" inm.cor_zona_n4_sec = %s")
			parametros.append(recibido["cor_zona_n4_sec"])
		if recibido["inm_tipoinmueble_sec"]  != "ALL":
			pedazosQuery.append(" inm.inm_tipoinmueble_sec = %s")
			parametros.append(recibido["inm_tipoinmueble_sec"])
		queryADD = " and inm_inmueble_precio between " + recibido["precioMin"] + " and " + recibido["precioMax"]
		queryADD += " and inm_inmueble_mtrsconstruccion between " + recibido["metrosMin"] + " and " + recibido["metrosMax"]
		queryADD += " and inm_inmueble_nro_hab >= " + recibido["habs"]
		queryADD += " and inm_inmueble_nro_banos >= " + recibido["banos"]
	for pedazo in pedazosQuery:
		queryADD += " and" + pedazo
		
	query0 += queryADD
	query += queryADD + " LIMIT " + recibido["nro_reg"] + " OFFSET " + recibidos["pos_inicio"]
	
	campos = ["inm_inmueble_sec", "inm_inmueble_desc", "inm_inmueble_operacion", "inm_tipoinmueble_sec", "inm_inmueble_precio", "inm_inmueble_canon_bsf",  "inm_inmueble_mtrsconstruccion", "inm_inmueble_nro_hab", "inm_inmueble_nro_banos", "pais", "estado", "ciudad", "zona"]	
	losDatosInmueble = eval(consultas(TK, query, campos, parametros, "consulta")+"")
	campos = ["nro_inmuebles"]
	parametros = []
	cantInmueble = eval(consultas(TK, query0, campos0 ,parametros0, "consulta")+"")	
	losDatosInmueble.append({'cant':[0]["nro_inmuebles"]})
	for elInmueble in losDatosInmueble:
		query2 = "select inm_inmueblefoto_ruta_nombre from inm_inmueble_fotos where inm_inmueble_sec = %s"
		campos2 = ["inm_inmueblefoto_ruta_nombre"]
		parametros2 = [elInmueble["inm_inmueble_sec"]]
		datosFotos = eval(consultas(TK, query2, campos2, parametros2, "consulta")+"")
		laFoto = "null"
		if len(datosFotos) > 0:
			laFoto = datosFotos[0]["inm_inmueblefoto_ruta_nombre"]
		elInmueble.update({"foto":laFoto})
		print "\n" + str(elInmueble) + "\n"
	return json.dumps(losDatosInmueble)

@route('/t_inm_inmueble_0001_calcula_nro_inmuebles_disponibles')
def t_inm_inmueble_0001_calcula_nro_inmuebles_disponibles():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select count(inm_inmueble_sec) as nro_inmuebles from inm_inmueble where inm_inmueble_compartida = 'P'"
	campos = ["nro_inmuebles"]
	parametros = []
	return consultas(TK, query, campos, parametros, "consulta")

@route('/t_inm_corredor_0001_calcula_nro_corredores_asociados')
def t_inm_corredor_0001_calcula_nro_corredores_asociados():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select count(login) as nro_corredores from cor_seg_users where active = 'S'"
	campos = ["nro_corredores"]
	parametros = []
	return consultas(TK, query, campos, parametros, "consulta")

@route('/t_inm_inmobiliaria_0001_calcula_nro_inmobiliarias_registradas')
def t_inm_inmobiliaria_0001_calcula_nro_inmobiliarias_registradas():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select count(inm_inmobiliaria_sec) as nro_inmobiliarias from inm_inmobiliaria"
	campos = ["nro_inmobiliarias"]
	parametros = []
	return consultas(TK, query, campos, parametros, "consulta")

@route('/t_inm_gvt_001_calcula_nro_gvt')
def t_inm_gvt_0001_calcula_nro_gvt():	
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select count(inm_gvt_sec) as nro_gvt  from inm_gvt where inm_gvt_propietario = %s"
	campos = ["nro_gvt"]
	parametros = [recibido["login"]]
	return consultas(TK, query, campos, parametros, "consulta")

@route('/t_cor_seg_users_0001_inserta_usuario')
def t_cor_seg_users_0001_inserta_usuario():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "insert into cor_seg_users values(%s,%s,%s,%s,'S','0','N',%s,%s,%s)"
	campos = []
	#fecha_actual = str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
	#fecha_actual += "-4:30"
	parametros = [recibido["login"], recibido["pswd"], recibido["name"], recibido["email"], recibido["active"], recibido["email_alternativo"], recibido["fecha_ingreso"], recibido["pagina_web"]]
	return consultas(TK, query, campos, parametros, "inserta")

@route('/t_inm_inmueble_fotos_0001_consulta_fotos')	
def t_inm_inmueble_fotos_0001_consulta_fotos():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select inm_inmueblefoto_ruta_nombre from inm_inmueble_fotos where inm_inmueble_sec = %s"
	campos = ["inm_inmueblefoto_ruta_nombre"]
	parametros = [recibido["inm_inmueble_sec"]]
	return consultas(TK, query, campos, parametros, "consulta")

@route('/t_inm_corredor_0001_consulta_corredor')
def t_inm_corredor_0001_consulta_corredor():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = """select corredor.login, corredor.inm_corredor_sec, corredor.inm_corredor_foto, corredor.inm_corredor_telf1, 
	corredor.inm_corredor_telf2, corredor.inm_profesion_sec, corredor.inm_corredor_anos_inicio, corredor.inm_inmobiliaria,
	usuario.name, usuario.email, usuario.active, usuario.email_alternativo from inm_corredor as corredor inner join 
	cor_seg_users as usuario on corredor.login = usuario.login where usuario.login = %s"""
	campos = ["login", "inm_corredor_sec", "inm_corredor_foto", "inm_corredor_telf1", "inm_corredor_telf2", "inm_profesion_sec", "inm_corredor_anos_inicio", "inm_inmobiliaria", "nombre", "email", "active", "email_alternativo"]
	parametros = [recibido["login"]]
	return consultas(TK, query, campos, parametros, "consulta")
	
@route('/t_inm_inmobiliaria_0001_consulta_inmobiliaria')
def t_inm_inmobiliaria_0001_consulta_inmobiliaria():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select * from inm_inmobiliaria"
	campos = ["login","inm_inmobiliaria_sec","inm_inmobiliaria_logotipo","inm_inmobiliaria_telf1","inm_inmobiliaria_telf2"]
	parametros = []
	return consultas(TK, query, campos, parametros, "consulta")

@post('/subir_imagen')
def subir():
	nombreSolicitado = request.forms.get('nombreLogo')
	losBytes = request.files.get('data')
	nombreArchivo = losBytes.filename		
	print "Archivo recibido: " + nombreArchivo
	raw = ""
	if losBytes.file:
		while True:
			datachunk = losBytes.file.read(1024)
			if not datachunk:
				break
			raw = raw + datachunk
	nuevoArchivo = open(directorio + '/images/' + nombreSolicitado +'.jpg','wb')
	nuevoArchivo.write(raw)
	nuevoArchivo.close()
	return "Titulo: %s Archivo original: %s Se subieron %d bytes." % (nombreSolicitado, nombreArchivo, len(raw))

@route('/t_inm_profesiones_0001_consulta_profesiones')
def t_inm_profesiones_0001_consulta_profesiones():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select inm_profesion_sec, inm_profesion_id from inm_profesiones where inm_profesion_activo = 'S'"
	campos = ["profesion_sec","profesion_id"]
	parametros = []
	return consultas(TK, query, campos, parametros, "consulta")
	
@route('/t_inm_especializacion_0001_inserta_zona_especializacion')
def t_inm_especializacion_0001_inserta_zona_especializacion():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "insert into inm_especializacion values(%s,%s,%s,%s,%s,%s)"
	campos = []
	conexion = psycopg2.connect(confBaseDatos)
	miCursor = conexion.cursor()
	miCursor.execute("select nextval('inm_especializacion_sec')")
	losDatos = miCursor.fetchall()
	parametros = [losDatos[0][0],recibido["login"], recibido["z1"], recibido["z2"], recibido["z3"], recibido["z4"]]
	return consultas(TK, query, campos, parametros, "inserta")

@route('/t_inm_corredor_0003_consulta_corredores_destacados')
def t_inm_corredor_0003_consulta_corredores_destacados():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = "select corr.inm_corredor_sec, corr.inm_corredor_foto, users.name FROM inm_corredor corr, cor_seg_users users WHERE corr.login = users.login AND  corr.login in ('Angel', 'Jose', 'Pedro', 'Tomas')"
	campos = ["codigo","foto","nombre"]
	parametros = []
	return consultas(TK, query, campos, parametros, "consulta")
	
@route('/t_inm_corredor_0004_consulta_corredores_detalles')
def t_inm_corredor_0004_consulta_corredores_detalles():
	recibido = dict(request.GET)
	TK = recibido["TK"]
	query = """	SELECT corr.inm_corredor_sec, corr.inm_corredor_foto, users.name, users.email, corr.inm_corredor_telf1, corr.inm_corredor_telf2, inm_inmobiliaria, prof.inm_profesion_id, corr.inm_corredor_anos_inicio 
				FROM inm_corredor corr JOIN cor_seg_users users ON corr.login = users.login LEFT JOIN inm_profesiones prof ON corr.inm_profesion_sec = prof.inm_profesion_sec
				WHERE corr.inm_corredor_sec = %s"""
	campos = ["codigo","foto","nombre","correo","telf1","telf2","empresa","profesion","ano_inicio_corredor"]
	parametros = [recibido["codigo"]]
	return consultas(TK, query, campos, parametros, "consulta")
	
@route('/favicon.ico')
def favicon():
	return static_file('iconoVentana.ico', root=directorio +"/images", mimetype="image/ico")

#run(host=socket.gethostname(), port=8001)
run(host='localhost', port=8000)