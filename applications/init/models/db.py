# -*- coding: utf-8 -*-
import datetime;
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig()

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.settings.actions_disabled=['register','request_reset_password','change_password','retrieve_username','profile']
#generate auth tabels.
auth.define_tables(username=True, signature=False)
db.auth_user.email.readable = db.auth_user.email.writable = False
db.auth_user.last_name.readable = db.auth_user.last_name.writable = False


# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)



#define tables
priority=range(1,200)
db.define_table('report_team',
	Field('name','string',length=50,label='报表归属',requires=IS_NOT_EMPTY()),
	Field('created_on','datetime',default=request.now),
	Field('ipaddr','string',length=50,default=request.client))

db.define_table('report_list',
	Field('team_id','string',length=50,label='报表归属'), 
	Field('name_zh','string',label='报表名称',requires=IS_NOT_EMPTY()), 
	Field('name','string',length=100,label='报表',requires=IS_NOT_EMPTY()),
	Field('priority','integer',label='优先级',requires=IS_IN_SET(priority)),
	Field('date_to','date',label='有效日期',requires=IS_DATE()),
	Field('created_on','datetime',default=request.now),
	Field('ipaddr','string',length=50,default=request.client))

db.define_table('report_visitor',
	Field('report_id','integer'),
	Field('user_name','string',length=20),
	Field('open_id','string',length=100),
	Field('visit_time','datetime',default=request.now),
	Field('ipaddr','string',label='IP',length=50,default=request.client))

db.define_table('comments',
	Field('report_id','integer'),
	Field('user_name','string',length=20),
	Field('usercomment','text',length=300,label='我的建议',requires=IS_NOT_EMPTY()),
	Field('issend','string',length=1,default='0'),
	Field('commit_time','datetime',default=request.now))
db.comments.id.readable = db.comments.id.writable = False
db.comments.report_id.readable = db.comments.report_id.writable = False
db.comments.user_name.readable = db.comments.user_name.writable = False
db.comments.commit_time.readable = db.comments.commit_time.writable = False


db.report_list.team_id.requires = IS_IN_DB(db,db.report_team.id,'%(name)s')
db.report_team.id.readable = db.report_team.id.writable = False
db.report_team.created_on.readable = db.report_team.created_on.writable = False
db.report_team.ipaddr.readable = db.report_team.ipaddr.writable = False
db.report_list.created_on.readable = db.report_list.created_on.writable = False
db.report_list.ipaddr.readable = db.report_list.ipaddr.writable = False

#回复建议表
db.define_table('replies',
	Field('comment_id',length=10),
	Field('replied','text',length=500,label='回复',requires=IS_NOT_EMPTY()),
	Field('issend','string',length=1,default='0'),
	Field('commit_time','datetime',default=request.now))
db.replies.id.readable = db.replies.id.writable = False
db.replies.comment_id.readable = db.replies.comment_id.writable = False
db.replies.commit_time.readable = db.replies.commit_time.writable = False
db.replies.issend.readable = db.replies.issend.writable = False

#定义表单
#form = SQLFORM.factory(db.comments)
#---------------中支列表
sql = "select trim(name) end from branch order by branch"
result = db.executesql(sql)
branchList = [ date[0] for date in result ]
filter_form_branch = SQLFORM.factory(
     Field('branch',label='中支',requires=IS_IN_SET(branchList),default=request.vars['branch']),
     )
timeList = [str(hour)+min for hour in range(8,23) for min in (':00',':30') ]

#用户信息
user_name = auth.user.username if auth.user else 'anonymous'
first_name = auth.user.first_name if auth.user else 'anonymous'
if not session.open_id:
    session.open_id = request.vars['openid'] or 'anonymous'

#定制消息模版表
db.define_table('msg_info',
	Field('msg','text',length=500,label='消息模版',requires=IS_NOT_EMPTY()),
	Field('definesql','text',length=500,label='sql语句',requires=IS_NOT_EMPTY()),
	Field('commit_time','datetime',default=request.now))
db.msg_info.id.readable = db.msg_info.id.writable = False
db.msg_info.commit_time.readable = db.msg_info.commit_time.writable = False

#定制消息列表
db.define_table('custom_msg',
	Field('msg_id','integer',label='消息模版',requires=IS_NOT_EMPTY()),
	Field('oa','string',length=50,label='用户OA',requires=IS_NOT_EMPTY(),default=user_name),
	Field('sendtime','time',length=50,label='发送时间',requires=IS_IN_SET(timeList)),
	Field('status','string',length=1,default='0'),
	Field('commit_time','datetime',default=request.now))
db.custom_msg.id.readable = db.custom_msg.id.writable = False
db.custom_msg.oa.readable = db.custom_msg.oa.writable = False
db.custom_msg.status.readable = db.custom_msg.status.writable = False
db.custom_msg.commit_time.readable = db.custom_msg.commit_time.writable = False
db.custom_msg.msg_id.requires = IS_IN_DB(db,db.msg_info.id,'%(msg)s')

#用户归属表
db.define_table('user_aracde',
	Field('oa','string',length=50,label='用户OA',unique=True,default=user_name),
	Field('aracde','string',length=3,label='所属机构CSC代码',default=''))
db.user_aracde.id.readable = db.user_aracde.id.writable = False
db.user_aracde.oa.requires = IS_NOT_IN_DB(db,db.user_aracde.oa)
db.user_aracde.aracde.requires=[IS_UPPER(),IS_NOT_EMPTY()]



#获取当前报表ID
table_id = request.args(0)[:9] if request.args(0) else 0

#添加评论
if request.vars.comment and auth.user:
    #防止重复提交
    if session.comment and session.comment==request.vars.comment:
        pass
    else:
        session.comment = request.vars.comment
        sql = """
        insert into comments(report_id,user_name,usercomment,commit_time,issend)values('%s','%s',trim('%s'),'%s','0')
        """ % (table_id,first_name,request.vars.comment,request.now)
        db.executesql(sql.decode('utf-8'))

#列出评论
sql = """
	SELECT
	a.id,
	report_id,
	USER_name,
	usercomment,
	a.commit_time AS q_time,
	comment_id,
	replied,
	b.commit_time AS a_time,
	b.id AS replied_id
	FROM
	comments a
	LEFT JOIN replies b ON
	a.ID = b.comment_id
	WHERE
	report_id = '%s'
	ORDER BY q_time desc,a_time limit 10
	""" % (table_id)
pagecomments=db.executesql(sql.decode('utf-8'))

#获取报表更新时间
sql="select data_time from data_time"
data_time=db.executesql(sql.decode('utf-8'))
update_time="数据更新时间:%s" % data_time[0][0].strftime("%Y-%m-%d %H:%M")

#insert visit log
sql = " insert into report_visitor(report_id,visit_time,ipaddr,user_name,open_id)values('%s','%s','%s','%s','%s') " % (table_id,request.now,request.client,user_name,session.open_id)
db.executesql(sql)





#业绩表-受理
db.define_table('ipe_hpad',
	Field('branch','string',length=2,label='中支',requires=IS_NOT_EMPTY()),
	Field('aracde','string',length=3,label='支公司',requires=IS_NOT_EMPTY()),
	Field('agntnum','string',length=8,label='工号',requires=IS_NOT_EMPTY()),
	Field('agntname','string',length=20,label='姓名',requires=IS_NOT_EMPTY()),
	Field('agtype','string',length=4,label='职级',requires=IS_NOT_EMPTY()),
	Field('chdrnum','string',length=8,label='保单号',requires=IS_NOT_EMPTY()),
	Field('trandate','decimal(8,0)',label='交易日期',requires=IS_NOT_EMPTY()),
	Field('cnttype','string',length=3,label='险种',requires=IS_NOT_EMPTY()),
	Field('acctamt','decimal(10,2)',label='规模保费',requires=IS_NOT_EMPTY()),
	Field('acctamt_std','decimal(10,2)',label='标准保费',requires=IS_NOT_EMPTY()),
	Field('commit_time','datetime',default=request.now))
#业绩表-当日受理
db.define_table('ipe_hpad_rt',
	Field('branch','string',length=2,label='中支',requires=IS_NOT_EMPTY()),
	Field('aracde','string',length=3,label='支公司',requires=IS_NOT_EMPTY()),
	Field('agntnum','string',length=8,label='工号',requires=IS_NOT_EMPTY()),
	Field('agntname','string',length=20,label='姓名',requires=IS_NOT_EMPTY()),
	Field('agtype','string',length=4,label='职级',requires=IS_NOT_EMPTY()),
	Field('chdrnum','string',length=8,label='保单号',requires=IS_NOT_EMPTY()),
	Field('trandate','decimal(8,0)',label='交易日期',requires=IS_NOT_EMPTY()),
	Field('cnttype','string',length=3,label='险种',requires=IS_NOT_EMPTY()),
	Field('acctamt','decimal(10,2)',label='规模保费',requires=IS_NOT_EMPTY()),
	Field('acctamt_std','decimal(10,2)',label='标准保费',requires=IS_NOT_EMPTY()),
	Field('commit_time','datetime',default=request.now))
#业绩表-预收
db.define_table('ipe_rtrn',
	Field('branch','string',length=2,label='中支',requires=IS_NOT_EMPTY()),
	Field('aracde','string',length=3,label='支公司',requires=IS_NOT_EMPTY()),
	Field('agntnum','string',length=8,label='工号',requires=IS_NOT_EMPTY()),
	Field('agntname','string',length=20,label='姓名',requires=IS_NOT_EMPTY()),
	Field('agtype','string',length=4,label='职级',requires=IS_NOT_EMPTY()),
	Field('chdrnum','string',length=8,label='保单号',requires=IS_NOT_EMPTY()),
	Field('trandate','decimal(8,0)',label='交易日期',requires=IS_NOT_EMPTY()),
	Field('cnttype','string',length=3,label='险种',requires=IS_NOT_EMPTY()),
	Field('acctamt','decimal(10,2)',label='规模保费',requires=IS_NOT_EMPTY()),
	Field('acctamt_std','decimal(10,2)',label='标准保费',requires=IS_NOT_EMPTY()),
	Field('commit_time','datetime',default=request.now))
#业绩表-当日预收
db.define_table('ipe_rtrn_rt',
	Field('branch','string',length=2,label='中支',requires=IS_NOT_EMPTY()),
	Field('aracde','string',length=3,label='支公司',requires=IS_NOT_EMPTY()),
	Field('agntnum','string',length=8,label='工号',requires=IS_NOT_EMPTY()),
	Field('agntname','string',length=20,label='姓名',requires=IS_NOT_EMPTY()),
	Field('agtype','string',length=4,label='职级',requires=IS_NOT_EMPTY()),
	Field('chdrnum','string',length=8,label='保单号',requires=IS_NOT_EMPTY()),
	Field('trandate','decimal(8,0)',label='交易日期',requires=IS_NOT_EMPTY()),
	Field('cnttype','string',length=3,label='险种',requires=IS_NOT_EMPTY()),
	Field('acctamt','decimal(10,2)',label='规模保费',requires=IS_NOT_EMPTY()),
	Field('acctamt_std','decimal(10,2)',label='标准保费',requires=IS_NOT_EMPTY()),
	Field('commit_time','datetime',default=request.now))
#业绩表-承保
db.define_table('ipe_acct',
	Field('branch','string',length=2,label='中支',requires=IS_NOT_EMPTY()),
	Field('aracde','string',length=3,label='支公司',requires=IS_NOT_EMPTY()),
	Field('agntnum','string',length=8,label='工号',requires=IS_NOT_EMPTY()),
	Field('agntname','string',length=20,label='姓名',requires=IS_NOT_EMPTY()),
	Field('agtype','string',length=4,label='职级',requires=IS_NOT_EMPTY()),
	Field('chdrnum','string',length=8,label='保单号',requires=IS_NOT_EMPTY()),
	Field('trandate','decimal(8,0)',label='交易日期',requires=IS_NOT_EMPTY()),
	Field('cnttype','string',length=3,label='险种',requires=IS_NOT_EMPTY()),
	Field('batc_type','string',length=10,label='类型',requires=IS_NOT_EMPTY()),
	Field('acctamt','decimal(10,2)',label='规模保费',requires=IS_NOT_EMPTY()),
	Field('acctamt_std','decimal(10,2)',label='标准保费',requires=IS_NOT_EMPTY()),
	Field('commit_time','datetime',default=request.now))
#业绩表-当日承保
db.define_table('ipe_acct_rt',
	Field('branch','string',length=2,label='中支',requires=IS_NOT_EMPTY()),
	Field('aracde','string',length=3,label='支公司',requires=IS_NOT_EMPTY()),
	Field('agntnum','string',length=8,label='工号',requires=IS_NOT_EMPTY()),
	Field('agntname','string',length=20,label='姓名',requires=IS_NOT_EMPTY()),
	Field('agtype','string',length=4,label='职级',requires=IS_NOT_EMPTY()),
	Field('chdrnum','string',length=8,label='保单号',requires=IS_NOT_EMPTY()),
	Field('trandate','decimal(8,0)',label='交易日期',requires=IS_NOT_EMPTY()),
	Field('cnttype','string',length=3,label='险种',requires=IS_NOT_EMPTY()),
	Field('batc_type','string',length=10,label='类型',requires=IS_NOT_EMPTY()),
	Field('acctamt','decimal(10,2)',label='规模保费',requires=IS_NOT_EMPTY()),
	Field('acctamt_std','decimal(10,2)',label='标准保费',requires=IS_NOT_EMPTY()),
	Field('commit_time','datetime',default=request.now))
#年度业绩
db.define_table('ipe_acct_year',
	Field('branch','string',length=2,label='中支',requires=IS_NOT_EMPTY()),
	Field('aracde','string',length=3,label='支公司',requires=IS_NOT_EMPTY()),
	Field('agntnum','string',length=8,label='工号',requires=IS_NOT_EMPTY()),
	Field('agntname','string',length=20,label='姓名',requires=IS_NOT_EMPTY()),
	Field('agtype','string',length=4,label='职级',requires=IS_NOT_EMPTY()),
	Field('chdrnum','string',length=8,label='保单号',requires=IS_NOT_EMPTY()),
	Field('trandate','decimal(8,0)',label='交易日期',requires=IS_NOT_EMPTY()),
	Field('cnttype','string',length=3,label='险种',requires=IS_NOT_EMPTY()),
	Field('batc_type','string',length=10,label='类型',requires=IS_NOT_EMPTY()),
	Field('acctamt','decimal(10,2)',label='规模保费',requires=IS_NOT_EMPTY()),
	Field('acctamt_std','decimal(10,2)',label='标准保费',requires=IS_NOT_EMPTY()),
	Field('commit_time','datetime',default=request.now))
#整合表——当月
db.define_table('agntinfo',
	Field('branch','string',length=2,label='中支',requires=IS_NOT_EMPTY()),
	Field('aracde','string',length=3,label='支公司',requires=IS_NOT_EMPTY()),
	Field('partnum','string',length=8,requires=IS_NOT_EMPTY()),
	Field('partname','string',length=100,requires=IS_NOT_EMPTY()),
	Field('teamnum','string',length=8,requires=IS_NOT_EMPTY()),
	Field('teamname','string',length=100,requires=IS_NOT_EMPTY()),
	Field('agntnum','string',length=8,requires=IS_NOT_EMPTY()),
	Field('agntname','string',length=100,requires=IS_NOT_EMPTY()),
	Field('agtype','string',length=4,requires=IS_NOT_EMPTY()),
	Field('dteapp','decimal(8,0)',requires=IS_NOT_EMPTY()),
	Field('dtetrm','decimal(8,0)',requires=IS_NOT_EMPTY()))
