# -*- coding: utf-8 -*-
import random
import os
import datetime
import time



#---------------------------------------------------------------------------------------------------------

@auth.requires_membership("admin")
def add_report_team():
    form = SQLFORM(db.report_team)
    if form.process().accepted:
        redirect(URL(add_report))
    return dict(form=form,return_message=update_time)

@auth.requires_membership("admin")
def add_report():
    form = SQLFORM(db.report_list,col3={'team_id':A('add',_href=URL('add_report_team'))})
    if form.process().accepted:
        redirect('index')
    elif form.errors:
        pass
    return dict(form=form)

@auth.requires_membership("admin")
def update_report():
    form=SQLFORM.grid(db.report_list)
    return dict(form=form)

@auth.requires_membership('admin')
def admin_user():
    form = SQLFORM.grid(db.auth_user)
    return dict(form=form)


@auth.requires_membership("admin")
def delete_comment():
    if request.args(0):
        sql = "delete from comments where id='%s' " % request.args(0)
	db.executesql(sql.decode('utf-8'))
    redirect(request.env.http_referer)

@auth.requires_membership("admin")
def delete_replies():
    if request.args(0):
        sql = "delete from replies where id='%s' " % request.args(0)
	db.executesql(sql.decode('utf-8'))
    redirect(request.env.http_referer)


#--------------------------------------------------------------------------------------------------------

@auth.requires_login()
def index():
    redirect(URL('main_page'))

@auth.requires_login()
def main_page():
    maxday = db.executesql("select max(trandate) as maxday from ipe_acct")
    lastday= datetime.datetime.now()-datetime.timedelta(days=1)
    currday= int(lastday.strftime("%Y%m%d"))
    monfirst= int(datetime.datetime.now().strftime("%d"))
    if currday != maxday[0][0] and int(request.now.strftime("%H"))>7 and monfirst != 1:
        return "<h1>总公司未推送业绩信息，请留意UC广播消息!</h1>"
    elif currday != maxday[0][0] and int(request.now.strftime("%H"))>5 and monfirst != 1:
        return "<h1>早上6点-8点是加工数据时间，此时间段系统将关闭访问，预计在8点左右开放!</h1>"
    #不允许直接访问
    page_title="报表目录"
    #报表目录
    sql_report_list = """
    select 
    name_zh, 
    a.name,
    a.id,
    0 as visit,
    b.id,
    date_to
      from report_list a,report_team b
          where date_format(date_to,'%Y-%m-%d')>date_format(NOW(),'%Y-%m-%d')
          and a.team_id=b.id
          order by priority ,visit desc
    """
    #数据正常
    result = db.executesql(sql_report_list.decode('utf-8'))
    return dict(result=result,page_title=page_title)

@auth.requires_login()
def main_page_new():
    response.flash="提示:《个险年度承保报表》已添加同期数据; 《个险当月受理、预收、承保业绩》已添加同期数据; 《支公司年度报表》已添加同期数据；《个险活动人力报表》已添加同期3千P人力数据."
    maxday = db.executesql("select max(trandate) as maxday from ipe_acct")
    lastday= datetime.datetime.now()-datetime.timedelta(days=1)
    currday= int(lastday.strftime("%Y%m%d"))
    monfirst= int(datetime.datetime.now().strftime("%d"))
    if currday != maxday[0][0] and int(request.now.strftime("%H"))>7 and monfirst != 1:
        return "<h1>总公司未推送业绩信息，请留意UC广播消息!</h1>"
    elif currday != maxday[0][0] and int(request.now.strftime("%H"))>5 and monfirst != 1:
        return "<h1>早上6点-8点是加工数据时间，此时间段系统将关闭访问，预计在8点左右开放!</h1>"
    #不允许直接访问
    page_title="报表目录"
    #报表目录
    sql_report_list = """
    select 
    name_zh, 
    a.name,
    a.id,
    0 as visit,
    b.id,
    date_to
      from report_list a,report_team b
          where date_format(date_to,'%Y-%m-%d')>date_format(NOW(),'%Y-%m-%d')
          and a.team_id=b.id
          order by priority ,visit desc
    """
    #数据正常
    result = db.executesql(sql_report_list.decode('utf-8'))
    return dict(result=result,page_title=page_title)


@auth.requires_login()
def user_aracde():
    form = SQLFORM(db.user_aracde)
    if form.process().accepted:
        redirect('index')
    elif form.errors:
        pass
    return dict(form=form)

@auth.requires_login()
def gx_ssyj_day():
    if int(request.now.strftime("%H")) < 8:
        return "当日实时业绩将于上午8点后开放。"
    report_name="个险当日受理、预收、承保业绩"
    tableHead=['中支','当日受理规模','当日受理标保','当日预收标保','当日承保标保']
    sql = """
	SELECT
	name,
	round(sl_yx_gm+sl_sz_gm,2),
	round(sl_yx_bb+sl_sz_bb,2),
	round(ys_yx_bb+ys_sz_bb,2),
	round(cb_yx_bb+cb_sz_bb,2),
	branch
	FROM
	bf_branch_day
	order by 2 desc
    """
    if user_name<>'it' or user_name<>'guoel':
        result=db.executesql(sql.decode('UTF-8'))
        return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:])
    else:
        return "报表正在测试中,请稍后查看."

@auth.requires_login()
def gx_ssyj_day_aracde():
    if int(request.now.strftime("%H")) < 8:
        return "当日实时业绩将于上午8点后开放。"
    report_name="个险当日受理、预收、承保业绩"
    tableHead=['支公司','当日受理规模','当日受理标保','当日预收标保','当日承保标保']
    if request.args(1):
        sql = """
        SELECT
        name,
        round(sl_yx_gm+sl_sz_gm,2),
        round(sl_yx_bb+sl_sz_bb,2),
        round(ys_yx_bb+ys_sz_bb,2),
        round(cb_yx_bb+cb_sz_bb,2),
        aracde
        FROM
        bf_aracde_day
	where branch='%s'
        order by 2 desc
        """ % request.args(1)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name,aracde=request.args(1))
    else:
        redirect(URL('gx_ssyj_day'))

@auth.requires_login()
def gx_ssyj_day_aracde_all():
    if int(request.now.strftime("%H")) < 8:
        return "当日实时业绩将于上午8点后开放。"
    report_name="全省支公司当日受理、预收、承保业绩"
    tableHead=['中支','支公司','当日受理标保','当日预收标保','当日承保标保']
    if request.args(0):
        sql = """
	select
	b.name,
	a.name,
	ifnull(round(sl_yx_bb+sl_sz_bb,2),0),
	ifnull(round(ys_yx_bb+ys_sz_bb,2),0),
	ifnull(round(cb_yx_bb+cb_sz_bb,2),0),
	b.branch
	from bf_aracde_day a,branch b
	where a.branch=b.branch
	order by 5 desc
        """ 
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,aracde=request.args(1))
    else:
        redirect(URL('gx_ssyj_day'))


@auth.requires_login()
def gx_ssyj_day_sl_list():
    tableHead=['支公司','保单号','标准保费','险种','代理人','职级']
    report_name="支公司当日受理保单清单"
    if (request.args(1) and request.args(2)):
        sql = """
        SELECT
        aracde,
        chdrnum,
        acctamt_std,
        ifnull(b.cnt_name,a.cnttype),
        agntname,
        agtype
        FROM ipe_hpad_rt a left join cnttype b on a.cnttype=b.code
	where aracde='%s'
	order by agntname,acctamt_std desc
        """ % (request.args(2))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect(gx_ssyj_day)

@auth.requires_login()
def gx_ssyj_day_ys_list():
    tableHead=['支公司','保单号','标准保费','险种','代理人','职级']
    report_name="支公司当日预收保单清单"
    if (request.args(1) and request.args(2)):
        sql = """
        SELECT
        aracde,
        chdrnum,
        acctamt_std,
        ifnull(b.cnt_name,a.cnttype),
        agntname,
        agtype
        FROM ipe_rtrn_rt a left join cnttype b on a.cnttype=b.code
	where aracde='%s'
	order by agntname,acctamt_std desc
        """ % (request.args(2))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect(gx_ssyj_day)

@auth.requires_login()
def gx_ssyj_day_cb_list():
    tableHead=['支公司','保单号','标准保费','险种','代理人','职级']
    report_name="支公司当日承保保单清单"
    if (request.args(1) and request.args(2)):
        sql = """
        SELECT
        aracde,
        chdrnum,
        acctamt_std,
        ifnull(b.cnt_name,a.cnttype),
        agntname,
        agtype
        FROM ipe_acct_rt a left join cnttype b on a.cnttype=b.code
	where aracde='%s'
	order by agntname,acctamt_std desc
        """ % (request.args(2))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect(gx_ssyj_day)


@auth.requires_login()
def gx_ssyj_mon():
    report_name="个险当月受理、预收、承保业绩(含当日)"
    tableHead=['中支','当月受理规模','当月受理标保','当月预收标保','当月承保标保','同期承保标保','增长率']
    sql = """
        SELECT
        name,
        round(sl_yx_gm+sl_sz_gm,0),
        round(sl_yx_bb+sl_sz_bb,0),
        round(ys_yx_bb+ys_sz_bb,0),
        round(cb_yx_bb+cb_sz_bb,0),
        round(b.bf,0),
        concat(round((cb_yx_bb+cb_sz_bb-b.bf)/b.bf*100,2),'%') as rate,
        a.branch
        FROM
        bf_branch_mon a left join tqyj_branch_mon b on a.branch=b.branch
        order by 2 desc
    """
    if user_name<>'it' or user_name<>'guoel':
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:],data_time=update_time)
    else:
        return "报表正在测试中,请稍后查看."

@auth.requires_login()
def gx_ssyj_mon_jan():
    report_name="个险当月受理、预收、承保业绩(1月2日--1月31日)"
    tableHead=['中支','当月受理规模','当月受理标保','当月预收标保','当月承保标保']
    sql = """
	SELECT
	name,
	round(sl_yx_gm+sl_sz_gm,2),
	round(sl_yx_bb+sl_sz_bb,2),
	round(ys_yx_bb+ys_sz_bb,2),
	round(cb_yx_bb+cb_sz_bb,2),
	branch
	FROM
	bf_branch_mon_jan
	order by 2 desc
    """
    if user_name<>'it' or user_name<>'guoel':
        result=db.executesql(sql.decode('UTF-8'))
        return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:])
    else:
        return "报表正在测试中,请稍后查看."


@auth.requires_login()
def gx_ssyj_mon_yx():
    if int(request.now.strftime("%H")) < 8:
        return "当日实时业绩将于上午8点后开放。"
    report_name="营销当月受理、预收、承保业绩(含当日)"
    tableHead=['中支','当月受理规模','当月受理标保','当月预收标保','当月承保标保']
    sql = """
	SELECT
	name,
	round(sl_yx_gm,1),
	round(sl_yx_bb,1),
	round(ys_yx_bb,1),
	round(cb_yx_bb,1),
	branch
	FROM
	bf_branch_mon
	order by 2 desc
    """
    if user_name<>'it' or user_name<>'guoel':
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:])
    else:
        return "报表正在测试中,请稍后查看."


@auth.requires_login()
def gx_ssyj_mon_sz():
    if int(request.now.strftime("%H")) < 8:
        return "当日实时业绩将于上午8点后开放。"
    report_name="收展当月受理、预收、承保业绩(含当日)"
    tableHead=['中支','当月受理规模','当月受理标保','当月预收标保','当月承保标保']
    sql = """
	SELECT
	name,
	round(sl_sz_gm,1),
	round(sl_sz_bb,1),
	round(ys_sz_bb,1),
	round(cb_sz_bb,1),
	branch
	FROM
	bf_branch_mon
	order by 2 desc
    """
    if user_name<>'it' or user_name<>'guoel':
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:])
    else:
        return "报表正在测试中,请稍后查看."





@auth.requires_login()
def gx_ssyj_mon_aracde():
    if int(request.now.strftime("%H")) < 8:
        return "当日实时业绩将于上午8点后开放。"
    report_name="个险当月受理、预收、承保业绩(含当日)"
    tableHead=['支公司','当月受理规模','当月受理标保','当月预收标保','当月承保标保']
    if request.args(1):
        sql = """
        SELECT
        name,
        round(sl_yx_gm+sl_sz_gm,2),
        round(sl_yx_bb+sl_sz_bb,2),
        round(ys_yx_bb+ys_sz_bb,2),
        round(cb_yx_bb+cb_sz_bb,2),
        aracde
        FROM
        bf_aracde_mon
	where branch='%s'
        order by 2 desc
        """ % request.args(1)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,aracde=request.args(1))
    else:
        redirect(URL('gx_ssyj_day'))

@auth.requires_login()
def gx_ssyj_mon_aracde_jan():
    if int(request.now.strftime("%H")) < 8:
        return "当日实时业绩将于上午8点后开放。"
    report_name="个险当月受理、预收、承保业绩(1月2日--1月31日)"
    tableHead=['支公司','当月受理规模','当月受理标保','当月预收标保','当月承保标保']
    if request.args(1):
        sql = """
        SELECT
        name,
        round(sl_yx_gm+sl_sz_gm,2),
        round(sl_yx_bb+sl_sz_bb,2),
        round(ys_yx_bb+ys_sz_bb,2),
        round(cb_yx_bb+cb_sz_bb,2),
        aracde
        FROM
        bf_aracde_mon_jan
	where branch='%s'
        order by 2 desc
        """ % request.args(1)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name,aracde=request.args(1))
    else:
        redirect(URL('gx_ssyj_day'))


@auth.requires_login()
def gx_ssyj_mon_aracde_all():
    if int(request.now.strftime("%H")) < 8:
        return "当日实时业绩将于上午8点后开放。"
    report_name="全省支公司当月受理、预收、承保业绩"
    tableHead=['中支','支公司','当月受理标保','当月预收标保','当月承保标保','标保排名']
    if request.args(0):
        sql = """
	select
	b.name,
	a.name,
	ifnull(round(sl_yx_bb+sl_sz_bb,2),0),
	ifnull(round(ys_yx_bb+ys_sz_bb,2),0),
	ifnull(round(cb_yx_bb+cb_sz_bb,2),0),
	b.branch
	from bf_aracde_mon a,branch b
	where a.branch=b.branch
	order by 5 desc
        """ 
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,aracde=request.args(1))
    else:
        redirect(URL('gx_ssyj_day'))



@auth.requires_login()
def gx_ssyj_mon_sl_list():
    tableHead=['保单号','交易日期','标准保费','险种','代理人','职级']
    if request.args(2):
        ara_name=db.executesql("select trim(name) from aracde where aracde='%s'" % request.args(2) )
    else:
        redirect(URL('index'))
    report_name="%s支公司当月受理清单" % ara_name[0]
    if (request.args(1) and request.args(2)):
        sql = """
        SELECT
        chdrnum,
	trandate,
        acctamt_std,
        ifnull(b.cnt_name,a.cnttype),
        agntname,
        agtype
        FROM ipe_hpad_mon a left join cnttype b on a.cnttype=b.code
	where aracde='%s'
	order by trandate,agntname,acctamt_std desc
        """ % (request.args(2))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect('index')

@auth.requires_login()
def gx_ssyj_mon_ys_list():
    tableHead=['保单号','交易日期','标准保费','险种','代理人','职级']
    if request.args(2):
        ara_name=db.executesql("select trim(name) from aracde where aracde='%s'" % request.args(2) )
    else:
        redirect(URL('index'))
    report_name="%s支公司当月预收清单" % ara_name[0]
    if (request.args(1) and request.args(2)):
        sql = """
        SELECT
        chdrnum,
	trandate,
        acctamt_std,
        ifnull(b.cnt_name,a.cnttype),
        agntname,
        agtype
        FROM ipe_rtrn_mon a left join cnttype b on a.cnttype=b.code
	where aracde='%s'
	order by trandate,agntname,acctamt_std desc
        """ % (request.args(2))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect('index')

@auth.requires_login()
def gx_ssyj_mon_cb_list():
    tableHead=['保单号','交易日期','标准保费','险种','代理人','职级']
    if request.args(2):
        ara_name=db.executesql("select trim(name) from aracde where aracde='%s'" % request.args(2) )
    else:
        redirect(URL('index'))
    report_name="%s支公司当月承保清单" % ara_name[0]
    if (request.args(1) and request.args(2)):
        sql = """
        SELECT
        chdrnum,
        trandate,
        acctamt_std,
        ifnull(b.cnt_name,a.cnttype),
        agntname,
        agtype
        FROM ipe_acct_mon a left join cnttype b on a.cnttype=b.code
	where aracde='%s'
	order by trandate,agntname,acctamt_std desc
        """ % (request.args(2))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect(URL('index'))

@auth.requires_login()
def gx_sl_cb_rl_day():
    report_name="[金泰杯]当日新增实动人力"
    tableHead=['中支','受理实动(3000P)','承保实动(3000P)','受理1万P人力','受理3万P人力','受理5万P人力']
    sql = """
	select
	  a.name,
	  b.rl_3_add,
	  c.rl_3_add,
	  b.rl_10_add,
	  b.rl_30_add,
	  b.rl_50_add,
	  a.branch
	  from branch a
	  left join addrl_branch_sl b on a.branch=b .branch
	  left join addrl_branch_cb c on a.branch=c .branch
	  order by 2 desc
    """
    if user_name<>'it' or user_name<>'guoel':
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:])
    else:
        return "报表正在测试中,请稍后查看."


@auth.requires_login()
def hdrl_add_list():
    if request.args(1) and request.args(2) and request.args(3):
	if request.args(3)=="sl":
            tableHead=['支公司','业务员','职级','当月标保','件数','当天标保']
            report_name="当日新增 %s P人力[受理]" % request.args(2)
	    table="slyj_agnt_list"
	elif request.args(3)=="cb":
            tableHead=['支公司','业务员','职级','当月标保','件数','当天标保']
            report_name="当日新增 %s P人力[承保]" % request.args(2)
	    table="cbyj_agnt_list"
        else:
	    pass
	sql = """
		SELECT
		c.name,
		b.agntname,
		b.agtype,
		a.bf,
		a.js,
		a.curr_bf
		FROM
		%s a,
		agntinfo b,
		aracde c
		WHERE
		a.agntnum=b.agntnum
		and b.aracde=c.aracde
		AND bf>=%s
		AND (bf-curr_bf)<%s
		and a.branch='%s'
		""" % (table,request.args(2),request.args(2),request.args(1))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,sql=sql)
    else:
        redirect(URL('index'))

@auth.requires_login()
def not_valide():
    report_name="受理未预收、预收未承保报表(含当日数据)"
    tableHead=['中支','受理未预收规保(万)','受理未预收件数','预收未承保标保(万)','预收未承保件数']
    sql = """
	select
	a.name,
	round(b.gmbf/10000,2),
	b.js,
	round(c.bb/10000,2),
	c.js,
	a.branch
	from branch a 
	left join not_rtrn_branch b on a.branch=b.branch
	left join not_acct_branch c on a.branch=c.branch
	order by 4 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:])

@auth.requires_login()
def not_valide_aracde():
    report_name="受理未预收、预收未承保报表(含当日数据)"
    tableHead=['中支','支公司','受理未预收规保(万)','受理未预收件数','预收未承保标保(万)','预收未承保件数']
    if (request.args(1)):
        if request.args(1)=='D':
 	    sql_arg=" where a.branch<>'D' order by 3 desc"
	else:
 	    sql_arg=" where a.branch='%s' order by 3 desc" % request.args(1)
        thissql = """
	select
	a.name,
	b.name,
	round(c.gmbf/10000,2),
	c.js,
	round(d.bb/10000,2),
	d.js,
        b.aracde
	from branch a
	left join aracde b on a.branch=b.branch 
	left join not_rtrn_aracde c on b.aracde=c.aracde
	left join not_acct_aracde d on b.aracde=d.aracde
        """ 
        sql=thissql+sql_arg
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,aracde=request.args(1))
    else:
        redirect(URL('index'))


@auth.requires_login()
def not_valide_rtrn_list():
    tableHead=['保单号','交易日期','标准保费','险种','代理人','职级']
    if request.args(2):
        ara_name=db.executesql("select trim(name) from aracde where aracde='%s'" % request.args(2) )
    else:
        redirect(URL('index'))
    report_name="%s支公司受理未预收清单" % ara_name[0]
    if (request.args(1) and request.args(2)):
        sql = """
	SELECT
	chdrnum,
	trandate,
	acctamt_std,
	cnt_name,
	agntname,
	agtype
	FROM
	not_in_rtrn
	where aracde='%s'
        order by trandate desc,agntname,acctamt_std desc
        """ % (request.args(2))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect(URL('index'))


@auth.requires_login()
def not_valide_acct_list():
    tableHead=['保单号','交易日期','标准保费','险种','代理人','职级']
    if request.args(2):
        ara_name=db.executesql("select trim(name) from aracde where aracde='%s'" % request.args(2) )
    else:
        redirect(URL('index'))
    report_name="%s支公司预收未承保清单" % ara_name[0]
    if (request.args(1) and request.args(2)):
        sql = """
	SELECT
	chdrnum,
	trandate,
	acctamt_std,
	cnt_name,
	agntname,
	agtype
	FROM
	not_in_acct
	where aracde='%s'
        order by trandate desc,agntname,acctamt_std desc
        """ % (request.args(2))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect(URL('index'))


@auth.requires_login()
def gx_sl_cb_rl():
    report_name="[金泰杯]当月受理、承保实动人力"
    tableHead=['中支','月初人力','受理3000P人力','受理实动率','承保3000P人力','承保实动率']
    sql = """
	select
	name,
	mon_rl,
	c.rl_3,
        concat(round(c.rl_3/mon_rl*100,2),'%'),
	d.rl_3,
        concat(round(d.rl_3/mon_rl*100,2),'%'),
	a.branch
	from branch a 
	left join rl_branch b on a.branch=b.branch
	left join hdrl_branch_sl c on a.branch=c.branch
	left join hdrl_branch_cb d on a.branch=d.branch
	order by 2 desc
    """
    if user_name<>'it' or user_name<>'guoel':
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:])
    else:
        return "报表正在测试中,请稍后查看."

@auth.requires_login()
def gx_sl_cb_rl_aracde():
    report_name="[金泰杯]当月受理、承保实动人力"
    tableHead=['中支','支公司','月初人力','受理3000P人力','受理实动率','承保3000P人力','承保实动率']
    if (request.args(1)):
        if request.args(1)=='D':
 	    sql_arg=" where a.branch<>'D' order by 3 desc"
	else:
 	    sql_arg=" where a.branch='%s' order by 3 desc" % request.args(1)
        thissql = """
        select
	a.name,
        b.name,
        c.mon_rl,
        d.rl_3,
        concat(round(d.rl_3/mon_rl*100,2),'%'),
        e.rl_3,
        concat(round(e.rl_3/mon_rl*100,2),'%')
        from branch a
        left join aracde b on a.branch=b.branch 
        left join rl_aracde c on b.aracde=c.aracde
        left join hdrl_aracde_sl d on b.aracde=d.aracde
        left join hdrl_aracde_cb e on b.aracde=e.aracde
        """ 
        sql=thissql+sql_arg
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect(URL('index'))



@auth.requires_login()
def gx_sl_cb_rl_wp():
    report_name="[金泰杯]当月受理、承保绩优人力"
    tableHead=['中支','受理万P人力','承保万P人力','受理3万P人力','承保3万P人力','受理5万P人力','承保5万P人力']
    sql="""
        select
        name,
        b.rl_10,
        c.rl_10,
        b.rl_30,
        c.rl_30,
        b.rl_50,
        c.rl_50,
        a.branch
        from branch a
        left join hdrl_branch_sl b on b.branch=a.branch
        left join hdrl_branch_cb c on c.branch=a.branch
        order by 2 desc
    """
    if user_name<>'it' or user_name<>'guoel':
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:])
    else:
        return "报表正在测试中,请稍后查看."

@auth.requires_login()
def gx_sl_cb_rl_wp_aracde():
    report_name="[金泰杯]当月受理、承保绩优人力"
    tableHead=['中支','支公司','受理万P人力','承保万P人力','受理3万P人力','承保3万P人力','受理5万P人力','承保5万P人力']
    if request.args(1):
        if request.args(1)=='D':
 	    sql_arg=" where a.branch<>'D' order by 3 desc"
	else:
 	    sql_arg=" where a.branch='%s' order by 3 desc" % request.args(1)
        sql="""
        select
 	d.name,
        a.name,
        b.rl_10,
        c.rl_10,
        b.rl_30,
        c.rl_30,
        b.rl_50,
        c.rl_50
        from aracde a
        left join hdrl_aracde_sl b on b.aracde=a.aracde
        left join hdrl_aracde_cb c on c.aracde=a.aracde
        left join branch d on d.branch=a.branch
        """ 
	sql = sql+sql_arg
        if user_name<>'it' or user_name<>'guoel':
            result=db.executesql(sql.decode('UTF-8'))
            return dict(result=result,tableHead=tableHead,report_name=report_name,pagecomments=pagecomments[:])
        else:
            return "报表正在测试中,请稍后查看."
    else:
        redirect(URL('index'))
#访问量
@auth.requires_membership("admin")
def visit_times():
    tableHead=['报表','当天访问次数','总访问次数']
    report_name="系统访问统计表"
    sql = """
	select
	  *
	  from(  
	select
	  report_name,
	  curr_times,
	  all_times,
	  report_id
	  from visit_times
	union 
	select
	  '合计访问次数',
	   sum(curr_times) as curr_times,
	   sum(all_times) as all_times,
	   0
	   from visit_times) a order by 3 desc 
    """
    all_comments=db.executesql(sql.decode('utf-8'))
    return dict(all_comments=all_comments,tableHead=tableHead,report_name=report_name)

#访问量
@auth.requires_membership("admin")
def visit_list():
    tableHead=['姓名','oa','open_id','访问时间','ipaddr']
    report_name="访问明细表(最近100次)"
    sql="select * from visit_list"
    all_comments=db.executesql(sql.decode('utf-8'))
    return dict(all_comments=all_comments,tableHead=tableHead,report_name=report_name)


@auth.requires_membership("admin")
def comment_list():
    tableHead=['建议','回复']
    report_name="建议列表"
    sql = """
	SELECT
        a.id,
        report_id,
        ifnull(c.NAME_ZH,'A'),
        ifnull(c.NAME,'main_page'),
        ifnull(USER_name,'A'),
        ifnull(userCOMMENT,'A'),
        a.commit_time AS q_time,
        ifnull(comment_id,'A'),
        ifnull(replied,''),
        b.commit_time AS a_time,
        b.id AS replied_id
	FROM
	comments a
	LEFT JOIN replies b ON a.ID = b.comment_id LEFT JOIN report_list c ON a.report_id=c.id
        ORDER BY q_time desc,a_time limit 20
    """
    all_comments=db.executesql(sql.decode('utf-8'))
    return dict(all_comments=all_comments,tableHead=tableHead,report_name=report_name)

@auth.requires_membership("admin")
def reply_comment():
    current_page = request.env.http_host+request.env.path_info
    if current_page != request.env.http_referer[7:].split('?')[0]:
        session.former_page = request.env.http_referer
    #添加回复
    db.replies.comment_id.default=request.args(0)
    form = SQLFORM(db.replies)
    if form.process().accepted:
        redirect(session.former_page)
    else:
        return dict(form=form,content=request.vars.content)


@auth.requires_login()
def bnk_tzrl_in13month():
    tableHead=['中支','一年内入司人力','留存人力','占比']
    report_name="银保续期13个月留存人力"
    sql = """
	SELECT
	a.name,
	b.rl,
	b.curr_rl,
	case when b.rl>0 then concat(round(b.curr_rl/b.rl*100,2),'%') else 0 end 
	from branch_bnk a left join bnk_tzrl_in13month b on a.branch=b.branch
	order by b.curr_rl/b.rl desc
	"""
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def bnk_tzrl_addrl():
    tableHead=['中支','月初人力','当月离职人力','当月新进人力','脱落率','净增员率']
    report_name="银保续期脱落人力及净增员率指标"
    sql = """
	SELECT  
	name,
	ycrl,
	hasgone,
	addrl,
	concat(round(hasgone/ycrl*100,2),'%'),
	concat(round((addrl-hasgone)/ycrl*100,2),'%')
	from branch_bnk a left join bnk_tzrl_addrl b on a.branch=b.branch
	order by 3 desc
	"""
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def bnk_tzrl_new_50():
    tableHead=['中支','今年入司且留存人力','当月5000P人力','占比']
    report_name="银保续期新人当月5000P转化率"
    sql = """
	SELECT  
	name,
	rl,
	rl_50,
	concat(round(rl_50/rl*100,2),'%') 
	from branch_bnk a left join bnk_tzrl_new_50 b on a.branch=b.branch
	order by 2 desc 
	"""
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def gx_bf_year():
    tableHead=['中支','承保标保(万)','件均保费(元)','同期标保(万)','同期件均(元)','标保增长率']
    report_name="全年_个险_承保业绩(含当日实时承保)"
    sql = """
	select
	a.name,
	round(b.bf,0),
	round(b.bf*10000/b.js,0),
        round(c.bf,0) as tqbf,
	round(c.bf*10000/c.js,0),
        concat(round((b.bf-c.bf)/c.bf*100,2),'%') as rate,
	a.branch
	from branch a 
	left join yj_branch_all b on a.branch=b.branch
        left join tqyj_branch_year c on a.branch=c.branch
	order by 2 desc
    """ 
    result=db.executesql(sql.decode('UTF-8'))
    return dict(data_time=update_time,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_bf_year_yx():
    tableHead=['中支','承保标保(万)','承保件数','件均保费(元)']
    report_name="全年_营销_承保业绩(含当日实时承保)"
    sql = """
	select
	a.name,
	round(b.yxbf,0),
	b.yxjs,
	round(b.yxbf*10000/b.yxjs,0),
	a.branch
	from branch a 
	left join yj_branch_all b on a.branch=b.branch
	order by 2 desc
    """ 
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_bf_year_sz():
    tableHead=['中支','承保标保(万)','承保件数','件均保费(元)']
    report_name="全年_收展_承保业绩(含当日实时承保)"
    sql = """
	select
	a.name,
	round(b.szbf,0),
	b.szjs,
	round(b.szbf*10000/b.szjs,0),
	a.branch
	from branch a 
	left join yj_branch_all b on a.branch=b.branch
	order by 2 desc
    """ 
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_bf_year_aracde():
    if request.args(1):
        if request.args(1)=='D':
            sql_parm=""
        else:
            sql_parm=" where a.branch='%s' " % request.args(1)
    else:
        return "非法访问"
    tableHead=['支公司','承保保费(万)','件均保费(元)','同期标保(万)','同比增长率','保费排名']
    report_name="全年_个险_支公司_承保业绩"
    sql = """
        select
        a.name,
        round(sum(b.bf)/10000,2),
        round(sum(b.bf)/sum(b.js),0),
        round(sum(c.bf)/10000,2),
        concat(round((sum(b.bf)-sum(c.bf))/sum(c.bf)*100,2),'%'),
        a.branch
        from aracde a 
        left join (select aracde,sum(bf) bf,sum(js) js from yj_aracde_all group by aracde) b on a.aracde=b.aracde
        left join (select aracde,sum(bf) bf,sum(js) js from tqyj_aracde_year group by aracde) c on a.aracde=c.aracde
  	{sql_parm}	
	group by a.name,a.branch
	order by 2 desc
    """ 
    sql=sql.format(sql_parm=sql_parm)
    result=db.executesql(sql.decode('UTF-8'))
    return dict(data_time=update_time,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_bf_year_aracde_yx():
    if request.args(1):
        branch=request.args(1)
    else:
        branch=""
    tableHead=['支公司','承保保费(万)','承保件数','件均标保(元)']
    report_name="全年_营销_支公司_承保业绩"
    sql = """
	select
	a.name,
	round(sum(b.yxbf)/10000,2),
	sum(b.yxjs),
	round(sum(b.yxbf)/sum(b.yxjs),0),
	a.branch
	from aracde a 
	left join yj_aracde_all b on a.aracde=b.aracde
	where a.branch='%s'
	group by a.name,a.branch
	order by 2 desc
    """ % branch
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_bf_year_aracde_sz():
    if request.args(1):
        branch=request.args(1)
    else:
        branch=""
    tableHead=['支公司','承保保费(万)','承保件数','件均标保(元)']
    report_name="全年_收展_支公司_承保业绩"
    sql = """
	select
	a.name,
	round(sum(b.szbf)/10000,2),
	sum(b.szjs),
	round(sum(b.szbf)/sum(b.szjs),0),
	a.branch
	from aracde a 
	left join yj_aracde_all b on a.aracde=b.aracde
	where a.branch='%s'
	group by a.name,a.branch
	order by 2 desc
    """ % branch
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def yb_dgx_ssyj_branch():
    tableHead=['中支','首期大个险','拓展大个险','大个险']
    report_name="银保当月大个险达成(含当日)"
    sql = """
	SELECT
	a.name,
	ifnull(ROUND(b.ape/10000,2),0),
	ifnull(ROUND(c.ape/10000,2),0),
	ROUND(ifnull(b.ape/10000,0)+ifnull(c.ape/10000,0),2)
	FROM
	branch_bnk a
	LEFT JOIN
	bf_branch_bnk_mon_sq b
	ON
	a.branch=b.branch
	LEFT JOIN
	bf_branch_bnk_mon_tz c
	ON
	a.branch=c.branch
	ORDER BY
	4 DESC
    """ 
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def yb_dgx_ssyj_branch_day():
    tableHead=['中支','首期大个险','拓展大个险','大个险']
    report_name="银保当日大个险达成"
    sql = """
	SELECT
	a.name,
	ifnull(ROUND(b.ape/10000,2),0),
	ifnull(ROUND(c.ape/10000,2),0),
	ROUND(ifnull(b.ape/10000,0)+ifnull(c.ape/10000,0),2),
	a.branch
	FROM
	branch_bnk a
	LEFT JOIN
	bf_branch_bnk_rt_sq b
	ON
	a.branch=b.branch
	LEFT JOIN
	bf_branch_bnk_rt_tz c
	ON
	a.branch=c.branch
	ORDER BY
	4 DESC
    """ 
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def yb_chdr_list():
    tableHead=['团队','业务员','渠道','保单号','险种','ape保费']
    report_name="当日保单承保明细"
    if request.args(1) and request.args(2):
        sql="""
          select
	  series,
	  agntname,
	  bnk_name,
	  chdrnum,
	  ifnull(cnt_name,'-'),
	  ape
	  from ipe_acct_bnk_rt a left join cnttype b on a.cnttype=b.code
	  where branch='%s' and series='%s' """ % (request.args(2),request.args(1))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect(URL('yb_dgx_ssyj_branch_day'))

@auth.requires_login()
def yb_hdrl_sq():
    report_name="银保首期活动人力报表"
    tableHead=['中支','当前人力','3000P人力','6000P人力','1万P人力','3万P人力','5万P人力']
    sql = """
        select
        name,
        curr_rl,
        rl_3,
        rl_6,
        rl_10,
        rl_30,
        rl_50
        from branch_bnk a
        left join rl_branch_bnk_sq b on a.branch=b.branch
        left join hdrl_branch_bnk_sq c on a.branch=c.branch
        order by 2 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def yb_hdrl_tz():
    report_name="银保拓展活动人力报表"
    tableHead=['中支','当前人力','3000P人力','6000P人力','1万P人力','3万P人力','5万P人力']
    sql = """
        select
        name,
        curr_rl,
        rl_3,
        rl_6,
        rl_10,
        rl_30,
        rl_50
        from branch_bnk a
        left join rl_branch_bnk_tz b on a.branch=b.branch
        left join hdrl_branch_bnk_tz c on a.branch=c.branch
        order by 2 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def gx_a71_all():
    report_name="鑫福年金指标分析_承保"
    tableHead=['中支','鑫福标保','标保占比','件数','件均保费','销售人力','销售人均件数']
    sql = """
	select
	name,
	round(a65_bf/10000,2),
	concat(round(bf_rate*100,2),'%'),
	js,
	round(avg_bf,0),
	rl,
	round(avg_js,2),
	a.branch
	from branch a left join a65_level_all_branch b on a.branch=b.branch
	order by 2 desc
	"""
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_a71_all_aracde():
    report_name="支公司鑫福年金指标分析_承保"
    tableHead=['支公司','标保','标保占比','件数','件均保费','销售人力','销售人均件数']
    if request.args(1):
        sql = """
	select
	name,
	round(a65_bf/10000,2),
	concat(round(bf_rate*100,2),'%'),
	js,
	round(avg_bf,0),
	rl,
	round(avg_js,2)
	from aracde a left join a65_level_all_aracde b on a.aracde=b.aracde
	{branch}
	order by 2 desc
        """
	if request.args(1)=='D':
	    sql_arg=""
 	else:
	    sql_arg=" where a.branch='%s'" % request.args(1)
	sql=sql.format(branch=sql_arg) 
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,aracde=request.args(1))
    else:
	return "未知参数"

@auth.requires_login()
def gx_a65_1():
    report_name="汇赢年金_小富康_指标分析"
    tableHead=['中支','汇赢标保','标保占比','件数','件均保费','销售人力','销售人均件数']
    sql = """
	select
	name,
	round(a65_bf/10000,2),
	concat(round(bf_rate*100,2),'%'),
	js,
	round(avg_bf,0),
	rl,
	round(avg_js,2),a.branch
	from branch a left join a65_level_1_branch b on a.branch=b.branch
	order by 2 desc
	"""
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_a65_1_aracde():
    report_name="汇赢年金_小富康_指标分析"
    tableHead=['支公司','汇赢标保','标保占比','件数','件均保费','销售人力','销售人均件数']
    if request.args(1):
        sql = """
	select
	name,
	round(a65_bf/10000,2),
	concat(round(bf_rate*100,2),'%'),
	js,
	round(avg_bf,0),
	rl,
	round(avg_js,2)
	from aracde a left join a65_level_1_aracde b on a.aracde=b.aracde
	{branch}
	order by 2 desc
        """
	if request.args(1)=='D':
	    sql_arg=""
 	else:
	    sql_arg=" where a.branch='%s'" % request.args(1)
	sql=sql.format(branch=sql_arg) 
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,aracde=request.args(1))
    else:
	return "未知参数"




@auth.requires_login()
def gx_a65_2():
    report_name="汇赢年金_大富康_指标分析"
    tableHead=['中支','汇赢标保','标保占比','件数','件均保费','销售人力','销售人均件数']
    sql = """
	select
	name,
	round(a65_bf/10000,2),
	concat(round(bf_rate*100,2),'%'),
	js,
	round(avg_bf,0),
	rl,
	round(avg_js,2),a.branch
	from branch a left join a65_level_2_branch b on a.branch=b.branch
	order by 2 desc
	"""
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_a65_2_aracde():
    report_name="汇赢年金_大富康_指标分析"
    tableHead=['支公司','汇赢标保','标保占比','件数','件均保费','销售人力','销售人均件数']
    if request.args(1):
        sql = """
	select
	name,
	round(a65_bf/10000,2),
	concat(round(bf_rate*100,2),'%'),
	js,
	round(avg_bf,0),
	rl,
	round(avg_js,2)
	from aracde a left join a65_level_2_aracde b on a.aracde=b.aracde
	{branch}
	order by 2 desc
        """
	if request.args(1)=='D':
	    sql_arg=""
 	else:
	    sql_arg=" where a.branch='%s'" % request.args(1)
	sql=sql.format(branch=sql_arg) 
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,aracde=request.args(1))
    else:
	return "未知参数"

#出勤报表20170927
@auth.requires_login()
def gx_cq_day_branch():
    if request.args(0)=="455":
        report_name="[ %s ]个险出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
	rl="pure_rl"
	cq=""
	next_page="456"
    elif request.args(0)=="463":
        report_name="[ %s ]营销出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
	rl="yx_rl"
	cq="yx_"
	next_page="465"
    elif request.args(0)=="464":
        report_name="[ %s ]收展出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
	rl="sz_rl"
	cq="sz_"
	next_page="466"
    else:
        return "参数错误!"
    tableHead=['中支','当前人力(不含CS\CA)','一次打卡人力','一次打卡出勤率','二次打卡人力','二次打卡出勤率']
    sql = """
	select 
	  name,
	  {rl},
	  {cq}cqrl,
	  concat(round({cq}cqrl/{rl}*100,2),'%'),
	  {cq}cqrl_2,
	  concat(round({cq}cqrl_2/{rl}*100,2),'%'),
	  a.branch
	  from branch a left join rl_branch b on a.branch=b.branch left join kq_day_branch c on a.branch=c.branch
	  order by cqrl/pure_rl desc
	"""
    sql=sql.format(rl=rl,cq=cq)
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name,next_page=next_page)

@auth.requires_login()
def gx_cq_day_aracde():
    if request.args(1):
        if request.args(0)=="456":
	    rl="pure_rl"
	    cq=""
	    next_page="457"
            report_name="[ %s ]个险出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        elif request.args(0)=="465":
	    rl="yx_rl"
	    cq="yx_"
	    next_page="467"
            report_name="[ %s ]营销出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        elif request.args(0)=="466":
	    rl="sz_rl"
	    cq="sz_"
	    next_page="468"
            report_name="[ %s ]收展出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        else:
            return "参数错误!"
        tableHead=['支公司','代码','当前人力(不含CS/CA)','一次打卡人力','一次打卡出勤率','二次打卡人力','二次打卡出勤率']
        sql = """
	select 
	  name,
	  a.aracde,
	  {rl},
	  {cq}cqrl,
	  concat(round({cq}cqrl/{rl}*100,2),'%'),
	  {cq}cqrl_2,
	  concat(round({cq}cqrl_2/{rl}*100,2),'%'),
	  a.aracde
	  from aracde a left join rl_aracde b on a.aracde=b.aracde left join kq_day_aracde c on a.aracde=c.aracde
	  where a.branch='{branch}'
	  order by cqrl/pure_rl desc
	"""
	sql=sql.format(branch=request.args(1),rl=rl,cq=cq)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,next_page=next_page)
    else:
	return "未知参数"

@auth.requires_login()
def gx_cq_day_part():
    if request.args(1):
        if request.args(0)=="457":
	    rl="pure_rl"
	    cq=""
	    next_page="458"
            report_name="[ %s ]个险出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        elif request.args(0)=="467":
	    rl="yx_rl"
	    cq="yx_"
	    next_page="469"
            report_name="[ %s ]营销出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        elif request.args(0)=="468":
	    rl="sz_rl"
	    cq="sz_"
	    next_page="470"
            report_name="[ %s ]收展出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        else:
            return "参数错误!"
        tableHead=['营业部','代码','当前人力(不含CS/CA)','一次打卡人力','一次打卡出勤率','二次打卡人力','二次打卡出勤率']
        sql = """
	select 
	  partname,
	  a.partnum,
	  {rl},
	  {cq}cqrl,
	  concat(round({cq}cqrl/{rl}*100,2),'%'),
	  {cq}cqrl_2,
	  concat(round({cq}cqrl_2/{rl}*100,2),'%'),
	  a.aracde,
	  a.partnum
	  from rl_part a left join kq_day_part b on a.aracde=b.aracde and a.partnum=b.partnum
	  where a.aracde='{aracde}'
	  order by cqrl/pure_rl desc  
	"""
	sql=sql.format(aracde=request.args(1),rl=rl,cq=cq)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name,next_page=next_page)
    else:
	return "未知参数"

@auth.requires_login()
def gx_cq_day_team():
    if request.args(1) and request.args(2):
        if request.args(0)=="458":
	    rl="pure_rl"
	    cq=""
            report_name="[ %s ]个险出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        elif request.args(0)=="469":
	    rl="yx_rl"
	    cq="yx_"
            report_name="[ %s ]营销出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        elif request.args(0)=="470":
	    rl="sz_rl"
	    cq="sz_"
            report_name="[ %s ]收展出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        else:
            return "参数错误!"
        tableHead=['营业组','代码','当前人力(不含CS/CA)','一次打卡人力','一次打卡出勤率','二次打卡人力','二次打卡出勤率']
        sql = """
	select 
	  teamname,
	  a.teamnum,
	  {rl},
	  {cq}cqrl,
	  concat(round({cq}cqrl/{rl}*100,2),'%'),
	  {cq}cqrl_2,
	  concat(round({cq}cqrl_2/{rl}*100,2),'%'),
	  a.aracde,
	  a.teamnum
	  from rl_team a left join kq_day_team b on a.aracde=b.aracde and a.teamnum=b.teamnum
	  where a.aracde='{aracde}' and a.partnum='{partnum}'
	  order by cqrl/pure_rl desc 
	"""
	sql=sql.format(aracde=request.args(1),partnum=request.args(2),rl=rl,cq=cq)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
	return "未知参数"

@auth.requires_login()
def gx_cq_day_list():
    if request.args(1) and request.args(2):
        report_name="[ %s ]出勤日报" % db.executesql('select max(kq_date) from kqinfo')[0]
        tableHead=['业务员','工号','职级','当日打卡次数']
        sql = """
	select
	agntname,
	a.agntnum,
	a.agtype,
	case when flag='有效' then 2  when flag='无效' then 1 else 0 end
	from     
	(SELECT
	*
	FROM
	agntinfo
	WHERE
	teamnum='%s'
	and aracde='%s'
	and dtetrm=99999999)a left join 
	(select
	*
	from kqinfo
	where  kq_date=(select max(kq_date) from kqinfo)  ) b on a.agntnum=b.agntnum
	order by 3 desc
	""" % (request.args(2),request.args(1))
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
	return "未知参数"



@auth.requires_login()
def taixx_branch():
    report_name="泰行销_用户当月登录统计表"
    tableHead=['中支','当前人力','当月登录人数','占比']
    sql = """
   select
        a.name,
        c.curr_rl,
        ifnull(dl_rl,0),
        concat(round(dl_rl/c.curr_rl*100,2),'%'),
        a.branch
        from branch a left join taixx_branch b on a.branch=b.branch left join rl_branch c on a.branch=c.branch
	order by dl_rl/c.curr_rl desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def taixx_aracde():
    if request.args(1):
        report_name="泰行销_用户当月登录统计表"
        tableHead=['支公司','登录人数']
        sql = """
	select
	name,
	ifnull(dl_rl,0),
	a.aracde
	from aracde a left join taixx_aracde b on a.aracde=b.aracde 
	where a.branch='%s'
	order by 2 desc
        """ % request.args(1)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        return "未知参数"

@auth.requires_login()
def taixx_list():
    if request.args(1):
        report_name="泰行销_当月登录用户"
        tableHead=['支公司代码','工号','姓名','职级']
        sql = """
	select
	b.aracde,
	b.agntnum,
	b.agntname,
	a.agtype
	from agntinfo a,taixx b where a.agntnum=b.agntnum
	and b.aracde='%s'
	""" % request.args(1)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        return "未知参数"



@auth.requires_login()
def taixx_branch_bnk():
    report_name="泰行销_银保团队当月登录统计表"
    tableHead=['中支','当月登录人数','其中:首期','其中:续期']
    sql = """
	select
        name,
        ifnull(dl_rl,0),
        ifnull(sq_rl,0),
        ifnull(tz_rl,0),
        a.branch
        from branch_bnk a left join taixx_branch_bnk b on a.branch=b.branch 
        order by 2 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def ycb_hpad_branch():
    report_name="2018年开泰杯预承保业绩_受理"
    tableHead=['中支','当天标保','当天件数','累计标保','累计件数']
    sql = """
        select
	  name,
	  convert(yj_day,decimal(10,2)),
	  js_day,
	  convert(bf,decimal(10,2)),
	  js,
	  a.branch
        from branch a left join ycb_hpad_branch b on a.branch=b.branch
        order by 4 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def ycb_hpad_aracde():
    if request.args(1): 
	sql="select name from branch where branch='%s'" % request.args(1)
        report_name="[ %s ]预承保业绩_受理" % db.executesql(sql)[0]
        if request.args(1)=="D":
	    where=""
        else:
	    where=" where a.branch='%s'" % request.args(1)
        tableHead=['支公司','当天标保','当天件数','累计标保','累计件数']
        sql = """
		SELECT
		name,
	        ifnull(convert(yj_day,decimal(10,2)),0),
	        ifnull(js_day,0),
	        ifnull(convert(bf,decimal(10,2)),0),
	        ifnull(js,0),
		a.branch
		FROM
		aracde a
		LEFT JOIN
		ycb_hpad_aracde b
		ON
		a.aracde=b.aracde
		{where}
		order by 4 desc
	"""
	sql=sql.format(where=where)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
	return "未知参数"

@auth.requires_login()
def ycb_rtrn_branch():
    report_name="2018年开泰杯预承保业绩_预收"
    tableHead=['中支','当天标保','当天件数','累计标保','累计件数']
    sql = """
        select
	  name,
	  ifnull(convert(yj_day,decimal(10,2)),0),
	  ifnull(js_day,0),
	  ifnull(convert(bf,decimal(10,2)),0),
	  ifnull(js,0),
	  a.branch
        from branch a left join ycb_rtrn_branch b on a.branch=b.branch
        order by 4 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def ycb_rtrn_aracde():
    if request.args(1): 
	sql="select name from branch where branch='%s'" % request.args(1)
        report_name="[ %s ]预承保业绩_预收" % db.executesql(sql)[0]
        if request.args(1)=="D":
	    where=""
        else:
	    where=" where a.branch='%s'" % request.args(1)
        tableHead=['支公司','当天标保','当天件数','累计标保','累计件数']
        sql = """
		SELECT
		name,
	        ifnull(convert(yj_day,decimal(10,2)),0),
	        ifnull(js_day,0),
	        ifnull(convert(bf,decimal(10,2)),0),
	        ifnull(js,0),
		a.branch
		FROM
		aracde a
		LEFT JOIN
		ycb_rtrn_aracde b
		ON
		a.aracde=b.aracde
		{where}
		order by 4 desc
	"""
	sql=sql.format(where=where)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
	return "未知参数"


@auth.requires_login()
def ycb_hpad_branch_sz():
    report_name="收展_2018年开泰杯预承保业绩_受理"
    tableHead=['中支','当天标保','当天件数','累计标保','累计件数']
    sql = """
        select
	  name,
	  ifnull(convert(yj_day,decimal(10,2)),0),
	  ifnull(js_day,0),
	  ifnull(convert(bf,decimal(10,2)),0),
	  ifnull(js,0),
	  a.branch
        from branch a left join ycb_hpad_branch_sz b on a.branch=b.branch
        order by 4 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def ycb_hpad_aracde_sz():
    if request.args(1): 
	sql="select name from branch where branch='%s'" % request.args(1)
        report_name="收展_[ %s ]预承保业绩_受理" % db.executesql(sql)[0]
        if request.args(1)=="D":
	    where=""
        else:
	    where=" where a.branch='%s'" % request.args(1)
        tableHead=['支公司','当天标保','当天件数','累计标保','累计件数']
        sql = """
		SELECT
		name,
	        ifnull(convert(yj_day,decimal(10,2)),0),
	        ifnull(js_day,0),
	        ifnull(convert(bf,decimal(10,2)),0),
	        ifnull(js,0),
		a.branch
		FROM
		aracde a
		LEFT JOIN
		ycb_hpad_aracde_sz b
		ON
		a.aracde=b.aracde
		{where}
		order by 4 desc
	"""
	sql=sql.format(where=where)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
	return "未知参数"



@auth.requires_login()
def ycb_rtrn_branch_sz():
    report_name="收展_2018年开泰杯预承保业绩_预收"
    tableHead=['中支','当天标保','当天件数','累计标保','累计件数']
    sql = """
        select
	  name,
	  ifnull(convert(yj_day,decimal(10,2)),0),
	  ifnull(js_day,0),
	  ifnull(convert(bf,decimal(10,2)),0),
	  ifnull(js,0),
	  a.branch
        from branch a left join ycb_rtrn_branch_sz b on a.branch=b.branch
        order by 4 desc 
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def ycb_rtrn_aracde_sz():
    if request.args(1): 
	sql="select name from branch where branch='%s'" % request.args(1)
        report_name="收展_[ %s ]预承保业绩_预收" % db.executesql(sql)[0]
        if request.args(1)=="D":
	    where=""
        else:
	    where=" where a.branch='%s'" % request.args(1)
        tableHead=['支公司','当天标保','当天件数','累计标保','累计件数']
        sql = """
		SELECT
		name,
	        ifnull(convert(yj_day,decimal(10,2)),0),
	        ifnull(js_day,0),
	        ifnull(convert(bf,decimal(10,2)),0),
	        ifnull(js,0),
		a.branch
		FROM
		aracde a
		LEFT JOIN
		ycb_rtrn_aracde_sz b
		ON
		a.aracde=b.aracde
		{where}
		order by 4 desc
	"""
	sql=sql.format(where=where)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
	return "未知参数"




@auth.requires_login()
def ycb_a71():
    report_name="2018年开门红预承保产品策略(受理)"
    tableHead=['中支','开门红标保','年金标保','年金占比','健康险标保','健康险占比','其它险种','占比']
    sql = """
	select
	  name,
	  all_bf,
	  a71,
	  a71_rate,
	  health,
	  health_rate,
	  other,
	  other_rate,
	  a.branch
	  from branch a left join ycb_a71 b on a.branch=b.branch
	  order by 2 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def ycb_rl_a71():
    report_name="2018年开门红 [预承保] 销售人力占比(受理)"
    tableHead=['中支','当前人力','实动人力(3000P)','占比','年金人力','年金人力占比','年金人力/实动人力']
    sql = """
	select
	  name,
	  curr_rl,
	  rl_30,
	  concat(convert(rl_30/curr_rl*100,decimal(10,0)),'%') rl_30_rate,
	  rl_a71,
	  concat(convert(rl_a71/curr_rl*100,decimal(10,0)),'%') rl_a71_rate,
	  concat(convert(rl_a71/rl_30*100,decimal(10,0)),'%') rl_a71_a30_rate,
	  a.branch
	  from branch a left join rl_branch b on a.branch=b.branch left join ycb_hpad_rl_branch c on a.branch=c.branch
	  order by 3 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def ycb_rl_rate():
    report_name="2018年开门红 [预承保] 实动率(受理)"
    tableHead=['中支','当前人力','1万P人力','占比','3万P人力','占比','5万P人力','占比']
    sql = """
	select
	  name,
	  curr_rl,
	  rl_100,
	  concat(convert(rl_100/curr_rl*100,decimal(10,1)),'%') rl_100_rate,
	  rl_300,
	  concat(convert(rl_300/curr_rl*100,decimal(10,1)),'%') rl_300_rate,
	  rl_500,
	  concat(convert(rl_500/curr_rl*100,decimal(10,1)),'%') rl_500_rate,
	  a.branch
	  from branch a left join rl_branch b on a.branch=b.branch left join ycb_hpad_rl_branch c on a.branch=c.branch
	  order by 3 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def ycb_rl_bmw():
    report_name="2018年开门红_全员抢宝马_预承保数据(受理)"
    tableHead=['中支','当前人力','实动人力(3000P)','占比','1.2万P人力','占比','1.2万P人力/实动人力']
    sql = """
	select
	  name,
	  curr_rl,
	  rl_30,
	  concat(convert(rl_30/curr_rl*100,decimal(10,1)),'%') rl_30_rate,
	  rl_120,
	  concat(convert(rl_120/curr_rl*100,decimal(10,1)),'%') rl_120_rate,
	  concat(convert(rl_120/rl_30*100,decimal(10,1)),'%') rl_120_30_rate,
	  a.branch
	  from branch a left join rl_branch b on a.branch=b.branch left join ycb_hpad_rl_branch c on a.branch=c.branch
	  order by 3 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_zgrl():
    report_name="个险主管实动报表"
    tableHead=['中支','主管人力(含收展主管)','经理人力(含收展经理)','当日新增3000P人力','当日新增经理实动','当月主管实动人力']
    sql = """
	select
	  a.name,
	  zgrl,
	  mgrl,
	  ifnull(curr_rl,0),
	  ifnull(curr_mgrl,0),
	  ifnull(rl,0),
	  a.branch
	  from branch a left join rl_zg_branch b on a.branch=b.branch left join yj_zg_branch c on a.branch=c.branch
	  order by 6 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def ycb_hpad_bnk_branch():
    report_name="银保预承保报表_受理"
    tableHead=['中支','当天标保','当天件数','累计标保','累计件数']
    sql = """
        select
	  name,
	  ifnull(convert(yj_day,decimal(10,2)),0),
	  ifnull(js_day,0),
	  ifnull(convert(bf,decimal(10,2)),0),
	  ifnull(js,0),
	  a.branch
        from branch a left join ycb_hpad_bnk_branch b on a.branch=b.branch
        order by 2 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)


@auth.requires_login()
def rrhs_branch():
    report_name="新春共享保费统计表"
    tableHead=['中支','共享件数','共享标保(万)']
    sql = """
	select
	name,
	ifnull(js,0),
	ifnull(round(bf/10000,2),0) as bf,
	a.branch
	from branch a left join rrhs_branch b on a.branch=b.branch
	order by 3 desc  
	"""
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def a75_branch():
    report_name="假日经营产品策略-健康百分百C件数占比"
    tableHead=['中支','3000P件数','3000P百分百C件数','占比']
    sql = """
	select
	name,
	ifnull(js_3,0),
	ifnull(js_a75,0),
	ifnull(rate,0),
	a.branch
	from branch a left join a75_branch b on a.branch=b.branch
	order by 3 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def a71_branch():
    report_name="假日经营产品策略-年金帐户件数占比"
    tableHead=['中支','6千件数','年金险件数','1.2万件数','帐户件数']
    sql = """
	select
	name,
	ifnull(js_6,0),
	ifnull(js_6_a71,0),
	js_12,
	js_12_a71, 
	a.branch
	from branch a left join a71_branch b on a.branch=b.branch
	order by 3 desc 
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def card_count():
    report_name="假日经营抢卡目标达成报表"
    tableHead=['中支','抢卡任务','抢卡人力','达成率','抢卡件数']
    sql = """
	select
	a.name,
	task,
	rl,
	concat(round(rl/task*100,2),'%'),
	js,
	a.branch
	from branch a
	left join card_task b on a.name=b.name
	left join card_count c on a.branch=c.branch
	order by 2 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)


















#now















@auth.requires_login()
def gx_rl_map():
    #判断是否完善机构代码
    sql="""
	select
	a.aracde,
	b.branch,
	trim(b.name),
	c.aracde,
	trim(c.name)
	from user_aracde a 
	left join branch b on a.aracde=b.branch
	left join aracde c on a.aracde=c.aracde
	where a.oa='%s'
    """ % user_name
    user_aracde=db.executesql(sql.decode('UTF-8'))
    if not user_aracde:
        redirect(URL('user_aracde'))
    else:
        if user_aracde[0][0]=='D':
	    sql_arg=""
            report_name="全省各职级人力分布图"
        elif len(user_aracde[0][0])==2:
	    sql_arg=" and branch='%s'" % user_aracde[0][0]
            report_name="%s各职级人力分布图" % user_aracde[0][2]
        elif len(user_aracde[0][0])==3:
	    sql_arg=" and aracde='%s'" % user_aracde[0][0]
            report_name="%s各职级人力分布图" % user_aracde[0][4]
	else:
            return "用户所属机构信息不存在."
    tableHead=['职级','当前人力']
    sql = """
	SELECT
	    *
	FROM
	    (
		SELECT
		    CASE
			WHEN CHAR_LENGTH(agtype)=4
			THEN 'RC'
			ELSE agtype
		    END            AS agtype,
		    COUNT(agntnum) AS rl
		FROM
		    agntinfo
		WHERE
		    dtetrm=99999999
		    %s
		GROUP BY
		    CASE
			WHEN CHAR_LENGTH(agtype)=4
			THEN 'RC'
			ELSE agtype
		    END
		UNION
		SELECT
		    '合计',
		    COUNT(agntnum) AS rl
		FROM
		    agntinfo
		WHERE
		    dtetrm=99999999 %s)a
	ORDER BY
	    CASE
		WHEN agtype='AD'
		THEN 1
		WHEN agtype='UM'
		THEN 2
		WHEN agtype='SS'
		THEN 3
		WHEN agtype='AS'
		THEN 4
		WHEN agtype='TS'
		THEN 5
		WHEN agtype='SA'
		THEN 6
		WHEN agtype='TA'
		THEN 17
		WHEN agtype='SD'
		THEN 8
		WHEN agtype='SE'
		THEN 9
		WHEN agtype='HD'
		THEN 0
		WHEN agtype='RC'
		THEN 12
		WHEN agtype='SM'
		THEN 11
		WHEN agtype='合计'
		THEN 30 
	    END
    """ % (sql_arg,sql_arg)
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def sz_rl_map():
    #判断是否完善机构代码
    sql="""
        select
        a.aracde,
        b.branch,
        trim(b.name),
        c.aracde,
        trim(c.name)
        from user_aracde a 
        left join branch b on a.aracde=b.branch
        left join aracde c on a.aracde=c.aracde
        where a.oa='%s'
    """ % user_name
    user_aracde=db.executesql(sql.decode('UTF-8'))
    if not user_aracde:
        redirect(URL('user_aracde'))
    else:
        if user_aracde[0][0]=='D':
            sql_arg=""
            report_name="全省各职级人力分布图"
        elif len(user_aracde[0][0])==2:
            sql_arg=" and branch='%s'" % user_aracde[0][0]
            report_name="%s各职级人力分布图" % user_aracde[0][2]
        elif len(user_aracde[0][0])==3:
            sql_arg=" and aracde='%s'" % user_aracde[0][0]
            report_name="%s各职级人力分布图" % user_aracde[0][4]
        else:
            return "用户所属机构信息不存在."
    tableHead=['职级','职级','当前人力']
    sql = """
	SELECT
	    b.name,
	    a.agtype,
	    a.rl
	FROM
	    (
		SELECT
		    SUBSTR(agtype,1,2) AS agtype,
		    COUNT(agntnum)     AS rl
		FROM
		    agntinfo
		WHERE
		    LENGTH(agtype)=4
		    and dtetrm=99999999
		    %s
		GROUP BY
		    SUBSTR(agtype,1,2))a
	LEFT JOIN
	    (
		SELECT
		    'SZ'  AS agtype,
		    '收展员' AS name
		UNION
		SELECT
		    'CA'     AS agtype,
		    '县域综合专员' AS name
		UNION
		SELECT
            'CS'    AS agtype,
            '续期督管员' AS name) b
	ON
	    a.agtype=b.agtype
        order by 3 desc
    """ % sql_arg
    sql_detail="""
        SELECT
            b.name,
            a.agtype,
            COUNT(agntnum) AS rl
        FROM
            agntinfo a left join xuqi_agtype b on a.agtype=b.agtype
        WHERE
            LENGTH(a.agtype)=4
        AND dtetrm=99999999
	%s
        GROUP BY
            a.agtype
        order by 3  desc
    """ % sql_arg
    result=db.executesql(sql.decode('UTF-8'))
    result1=db.executesql(sql_detail.decode('UTF-8'))
    return dict(result1=result1,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_hdrl_branch():
    report_name="个险当月活动人力报表"
    tableHead=['中支','3千P人力','同期3千P(不含当日)','6千P人力','1万P人力','3万P人力','5万P人力']
    sql = """
	select
	name,
	rl_3,
	yx+sz,
	rl_6,
	rl_10,
	rl_30,
	rl_50,
	a.branch
	from branch a
	left join hdrl_branch_cb b on a.branch=b.branch
        left join tqhdrl_branch c on a.branch=c.branch
	order by 2 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(data_time=update_time,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_login()
def gx_hdrl_branch_jan():
    report_name="个险活动人力报表(1月2日--1月31日)"
    tableHead=['中支','3000P人力','6000P人力','1万P人力','3万P人力','5万P人力']
    sql = """
	select
	name,
	rl_3,
	rl_6,
	rl_10,
	rl_30,
	rl_50,
	a.branch
	from branch a
	left join hdrl_branch_cb_jan b on a.branch=b.branch
	order by 2 desc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(update_time=update_time,result=result,tableHead=tableHead,report_name=report_name)



@auth.requires_login()
def gx_hdrl_aracde():
    report_name="个险活动人力报表"
    tableHead=['支公司','3000P人力','6000P人力','1万P人力','3万P人力','5万P人力']
    if request.args(1):
        sql = """
	select
	name,
	rl_3,
	rl_6,
	rl_10,
	rl_30,
	rl_50,
	a.branch
	from aracde a
	left join hdrl_aracde_cb b on a.aracde=b.aracde
	where a.branch='%s'
	order by 2 desc
        """ % request.args(1)
        result=db.executesql(sql.decode('UTF-8'))
        return dict(result=result,tableHead=tableHead,report_name=report_name)
    else:
        redirect(URL('gx_hdrl_branch'))


@auth.requires_login()
def my_msg():
    #判断是否完善机构代码
    user_aracde=db.executesql("select aracde from user_aracde where oa='%s'" % user_name)
    if not user_aracde:
        redirect(URL('user_aracde'))
    #表单
    form = SQLFORM(db.custom_msg)
    if form.process().accepted:
        redirect(URL('my_msg',args=429))
    elif form.errors:
	return form.errors
    #更新开关
    if request.args(1):
        sql = """
        UPDATE custom_msg SET status=(CASE WHEN status = '1' OR status IS NULL THEN '0' ELSE '1' end)
          WHERE id=%s
        """ % request.args(1) or 0
        db.executesql(sql.decode('UTF-8'))
    sql="""
	select
	msg,
	b.sendtime,
	case when status='0' then '正常' else '禁用' end,
        b.commit_time ,
        b.id
	from msg_info a,custom_msg b
	where a.id=b.msg_id
	and b.oa='%s'
        order by 4 desc
    """ % user_name
    result=db.executesql(sql.decode('UTF-8'))
    report_name="定制推送消息"
    tableHead=['消息','推送时间','状态','定制时间']
    return dict(form=form,result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_membership('admin')
def msg_info():
    form = SQLFORM.grid(db.msg_info)
    return dict(form=form)

def test():
    return dict(group=auth.user_groups.values())


@auth.requires_login()
def report_request():
    return dict(report_name="需求列表")


#----------------------------------------------------------------------------------------------------------------------------
#监控报表
#----------------------------------------------------------------------------------------------------------------------------

@auth.requires_membership('it')
def jf_wendu():
    form = SQLFORM.factory(
           Field('floor_name',label='机房',
           requires=IS_IN_SET(['6楼电销','11楼','13楼','13楼_2','鹤壁','周口','开封','新乡','漯河',
           '三门峡','洛阳','南阳','信阳','商丘','郑州','平顶山','濮阳','驻马店','安阳','许昌','焦作','洛阳电销']),
           default=request.vars['floor_name']))
    if request.vars['floor_name']=='11楼':
        jifang_id = '11F_FGS'
    elif request.vars['floor_name']=='开封':
        jifang_id = 'KF'
    elif request.vars['floor_name']=='商丘':
        jifang_id = 'SQ'
    elif request.vars['floor_name']=='安阳':
        jifang_id = 'AY'
    elif request.vars['floor_name']=='鹤壁':
        jifang_id = 'HB'
    elif request.vars['floor_name']=='焦作':
        jifang_id = 'JZ'
    elif request.vars['floor_name']=='洛阳':
        jifang_id = 'LY'
    elif request.vars['floor_name']=='漯河':
        jifang_id = 'LH'
    elif request.vars['floor_name']=='南阳':
        jifang_id = 'NY'
    elif request.vars['floor_name']=='平顶山':
        jifang_id = 'PDS'
    elif request.vars['floor_name']=='濮阳':
        jifang_id = 'PY'
    elif request.vars['floor_name']=='三门峡':
        jifang_id = 'SMX'
    elif request.vars['floor_name']=='新乡':
        jifang_id = 'XX'
    elif request.vars['floor_name']=='信阳':
        jifang_id = 'XY'
    elif request.vars['floor_name']=='许昌':
        jifang_id = 'XC'
    elif request.vars['floor_name']=='郑州':
        jifang_id = 'ZZ'
    elif request.vars['floor_name']=='周口':
        jifang_id = 'ZK'
    elif request.vars['floor_name']=='驻马店':
        jifang_id = 'ZMD'
    elif request.vars['floor_name']=='洛阳电销':
        jifang_id = 'LYDX'
    elif request.vars['floor_name']=='6楼电销':
        jifang_id = '6F_DX'
    elif request.vars['floor_name']=='13楼':
        jifang_id = '13F_FGS_1'
    elif request.vars['floor_name']=='13楼_2':
        jifang_id = '13F_FGS_2'
    else:
        jifang_id = 't'
    report_name="机房温湿度监控报表"
    tableHead=['机房代码','温度','露点','湿度','采集时间']
    if request.vars['floor_name']:
            sql = """
                select
		*
		from tem63
                where flr ='%s'
		order by 5 desc
            """ % jifang_id
            result=db.executesql(sql.decode('UTF-8'))
    else:
            result=""
    return dict(result=result,tableHead=tableHead,report_name=report_name,form=form)

@auth.requires_membership('it')
def ups():
    report_name="UPS监控报表"
    tableHead=['UPS','输入电压','输出电压','采集时间',]
    sql="""
	select * from apc
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

@auth.requires_membership('it')
def netstat():
    report_name="网络状态监控"
    tableHead=['名称','状态']
    sql="""
        select * from nodes63 order by 2 
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)




#其它报表
@auth.requires_login()
def yb_value():
    report_name="银保新单价值数据(截止上月)"
    tableHead=['中支','名称','月份','价值保费(万)']
    sql="""
	select
	a.branch,
	b.name,
	round(trandate/100,0),
	round(sum(acctamt_std)/10000,2)
	from ipe_acct_bnk_year a left join branch_bnk b on a.branch=b.branch
	group by a.branch,b.name,round(trandate/100,0)
    """
    result=db.executesql(sql.decode('UTF-8'))
    return dict(result=result,tableHead=tableHead,report_name=report_name)

def kqinfo():
    return ""
    #Field('YourDate','date',label='选择日期',requires=IS_NOT_EMPTY()))
    result=db().select(db.agntinfo.ALL)
    return dict(result=result)
    











def download():
    return response.download(request,db)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def search():
    """an ajax wiki search page"""
    return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
        _onkeyup="ajax('callback',['keyword'],'target');")),
        target_div=DIV(_id='target'))


def callback():
    """an ajax callback that return a <ul> of links to wiki pages"""
    query = db.page.title.contains(request.vars.keyword)
    pages = db(query).select(orderby=db.page.title)
    links = [A(p.title+p.body, _href=URL('show',args=p.id)) for p in pages]
    return UL(links)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


