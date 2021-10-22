from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from mysql_util import MysqlUtil
from passlib.hash import sha256_crypt
from functools import wraps
import time
from forms import Dormitory_Form,Linkman_Form,Order_Form

app=Flask(__name__) #创建应用

#用户注册
@app.route('/register',methods=['GET','POST'])
def register():
    form=Dormitory_Form(request.form)#实例化表单类
    if request.method=='POST':#如果提交表单
        #获取字段内容
        school_name=form.school_name.choices[int(request.form.get('school'))][1]
        dormitory_number=form.dormitory_number.choices[int(request.form.get('home'))][1]
        room_number=form.room_number.data
        email=form.email.data
        password=form.password.data
        db=MysqlUtil() #实例化数据库操作类
        sql="INSERT INTO dormitory(school_name,dormitory_number,room_number,email,password)\
            VALUES('%s','%s','%s','%s','%s')"%(school_name,dormitory_number,room_number,email,password)#user表中插入记录
        db.insert(sql)
        flash('您已注册成功，请登录','success')#闪存信息
        return redirect(url_for('login')) # 跳转到登录页面

    return render_template('register.html',form=form)#渲染模板

#用户登录
@app.route('/login',methods=['GET','POST'])
def login():
    if "logged_in" in session: #如果已经登录，则直接跳转到控制台
        return redirect(url_for("dashboard"))

    if request.method=="POST": #如果提交表单
        # 从表单中获取字段
        email=request.form['email']
        password_candidate=request.form['password']
        sql="SELECT * FROM dormitory WHERE email='%s'"%(email) #根据用户名查找user表中记录
        db=MysqlUtil() #实例化数据库操作类
        result=db.fetchone(sql) #获取一条记录
        if result: #如果查到记录
            dormitory_id=result['dormitory_id']
            password=result['password'] #用户注册时填写的密码
            #对比用户登录时填写的密码和数据库中记录的密码是否一致
            if password_candidate==password: #调用verify方法验证，如果为真，则通过
                #写入session
                session['logged_in']=True
                session['email']=email
                flash('登录成功！','success') #闪存信息
                if email=='884664869@qq.com':
                    return redirect(url_for('dashboard')) #跳转到控制台
                else:
                    return redirect('/logined_in/{}'.format(dormitory_id))
            else: #如果密码错误
                error='邮箱与密码不匹配'
                return render_template('login.html',error=error) #跳转到登录页，并提示错误信息
        else:
            error='该邮箱未注册'
            return render_template('login.html',error=error)

    return render_template('login.html')

#is_logged_in装饰器
# 如果用户已经登录
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:     # 判断用户是否登录
            return f(*args, **kwargs)  # 如果登录，继续执行被装饰的函数
        else:                          # 如果没有登录，提示无权访问
            flash('无权访问，请先登录', 'danger')
            return redirect(url_for('login'))
    return wrap

#普通用户界面
@app.route('/logined_in/<string:dormitory_id>',methods=['GET','POST'])
@is_logged_in
def logined_in(dormitory_id):
    db=MysqlUtil() #实例化数据库操作类
    sql1="SELECT *FROM dormitory where dormitory_id=%s"%(dormitory_id) #查找用户信息
    result1=db.fetchone(sql1) #查找该用户信息
    db=MysqlUtil() #实例化数据库操作类
    sql2="SELECT *FROM linkman where dormitory_id=%s"%(dormitory_id)
    result2=db.fetchall(sql2)
    if not result2: #如果未设定联系人
        result2=[{'linkman_name':'无','linkman_email':'无'}]
    db=MysqlUtil()
    sql3="SELECT *FROM order_form where dormitory_id=%s ORDER BY create_time DESC"%(dormitory_id)
    result3=db.fetchall(sql3)
    order=[]
    for i in range(len(result3)):
        order_date=result3[i]['preset_day'].strftime('%Y-%m-%d')
        order_time=result3[i]['preset_time']
        create_time=result3[i]['create_time']
        water_brand=result3[i]['water_brand']
        water_number=result3[i]['water_number']
        db=MysqlUtil()
        sql="SELECT water_price FROM water where water_brand='%s'"%(water_brand)
        water_price=int(db.fetchone(sql)['water_price'])
        order_price=water_price*water_number
        temp_order={'create_time':create_time,'preset_time':order_date+order_time,'water_brand':water_brand,'water_number':water_number,'order_price':order_price}
        order.append(temp_order)
    return render_template('logined_in.html',dormitory=result1,linkman=result2,order=order)

#普通用户修改个人信息界面
@app.route('/logined_in/<string:dormitory_id>/edit',methods=['GET','POST'])
@is_logged_in
def logined_in_edit(dormitory_id):
    db=MysqlUtil() #实例化数据库操作类
    sql1="SELECT *FROM dormitory where dormitory_id=%s"%(dormitory_id) #查找用户信息
    result1=db.fetchone(sql1) #查找该用户信息
    db=MysqlUtil() #实例化数据库操作类
    sql2="SELECT *FROM linkman where dormitory_id=%s"%(dormitory_id)
    result2=db.fetchall(sql2)
    form=Linkman_Form(request.form)#实例化表单类
    if request.method=='POST'and form.validate():#如果提交表单
        #获取字段内容
        linkman_name=form.linkman_name.data
        linkman_email=form.linkman_email.data
        db=MysqlUtil() #实例化数据库操作类
        sql="INSERT INTO linkman(dormitory_id,linkman_name,linkman_email) VALUES('%s','%s','%s')"%(dormitory_id,linkman_name,linkman_email)#user表中插入记录
        db.insert(sql)
        flash('修改成功','success')#闪存信息
        return redirect(url_for('logined_in',dormitory_id=dormitory_id)) # 跳转到登录页面
    return render_template('logined_in_edit.html',dormitory=result1,linkman=result2)

#普通用户添加联系人界面
@app.route('/logined_in/<string:dormitory_id>/add',methods=['GET','POST'])
@is_logged_in
def logined_in_add(dormitory_id):
    db=MysqlUtil() #实例化数据库操作类
    sql="SELECT *FROM linkman where dormitory_id=%s"%(dormitory_id)
    result=db.fetchall(sql)
    form=Linkman_Form(request.form)#实例化表单类
    if request.method=='POST'and form.validate():#如果提交表单
        #获取字段内容
        linkman_name=form.linkman_name.data
        linkman_email=form.linkman_email.data
        db=MysqlUtil() #实例化数据库操作类
        sql="INSERT INTO linkman(dormitory_id,linkman_name,linkman_email) VALUES('%s','%s','%s')"%(dormitory_id,linkman_name,linkman_email)#user表中插入记录
        db.insert(sql)
        flash('修改成功','success')#闪存信息
        return redirect(url_for('logined_in',dormitory_id=dormitory_id)) # 跳转到登录页面
    return render_template('logined_in_add.html',linkman=result)

#普通用户订水界面
@app.route('/logined_in/<string:dormitory_id>/order',methods=['GET','POST'])
@is_logged_in
def order(dormitory_id):
    form=Order_Form(request.form)#实例化表单类
    if request.method=='POST'and form.validate:#如果提交表单
        order_date=request.form['order_date']
        order_time=form.order_time.choices[int(request.form.get('order_time'))][1]
        water_brand=form.water_brand.choices[int(request.form.get('water_brand'))][1]
        water_number=int(form.water_number.choices[int(request.form.get('water_number'))][1][0])
        create_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        #1创建订单
        db=MysqlUtil()
        sql="INSERT INTO order_form(dormitory_id,water_brand,water_number,create_time,preset_day,preset_time) \
             VALUES('%s','%s',%d,'%s','%s','%s')"%(dormitory_id,water_brand,water_number,create_time,order_date,order_time)
        db.insert(sql)
        #2更新库存
        db=MysqlUtil()
        sql="UPDATE water SET water_stock=water_stock-%d WHERE water_brand='%s'" %(water_number,water_brand)
        db.update(sql)
        #3更新余额
        db=MysqlUtil()
        sql="SELECT water_price FROM water where water_brand='%s'"%(water_brand)
        water_price=int(db.fetchone(sql)['water_price'])
        order_price=water_price*water_number
        db=MysqlUtil()
        sql="UPDATE dormitory SET banlance=banlance-%d WHERE dormitory_id='%s'" %(order_price,dormitory_id)
        db.update(sql)
        flash('提交订单成功','success')#闪存信息
        return redirect(url_for('logined_in',dormitory_id=dormitory_id)) # 跳转到登录页面
    return render_template('logined_in_order.html')



#控制台
@app.route('/dashboard')
@is_logged_in
def dashboard():
    #获取宿舍信息
    db=MysqlUtil() #实例化数据库操作类
    sql="SELECT *FROM dormitory" #查找用户信息
    result1=db.fetchall(sql) #查找所有用户
    #获取订单信息
    db=MysqlUtil()
    sql="SELECT *FROM order_form ORDER BY preset_day DESC"
    result2=db.fetchall(sql)
    if result2:
        new_day=result2[0]['preset_day']
        all_order=[]
        for i in range(len(result2)):
            temp_id=result2[i]['dormitory_id']
            temp_preset_day=result2[i]['preset_day'].strftime("%Y-%m-%d")
            temp_preset_time=result2[i]['preset_time']
            temp_brand=result2[i]['water_brand']
            temp_number=result2[i]['water_number']
            for j in range(len(result1)):
                if result1[j]['dormitory_id']==temp_id:
                    temp_dormitory=result1[j]['dormitory_number']
                    temp_school=result1[j]['school_name']
                    break
            temp_order={'school_name':temp_school,'dormitory_number':temp_dormitory,'water_brand':temp_brand,'water_number':temp_number,'preset_time':temp_preset_day+temp_preset_time}
            all_order.append(temp_order)
    else:
        all_order=[]
    
    return render_template('dashboard.html',dormitory=result1,orders=all_order)

 
#查看宿舍功能
@app.route('/edit_dormitory/<string:dormitory_id>',methods=['GET','POST'])
@is_logged_in
def edit_dormitory(dormitory_id):
    db=MysqlUtil() #实例化数据库操作类
    sql1="SELECT *FROM dormitory where dormitory_id=%s"%(dormitory_id) #查找用户信息
    result1=db.fetchone(sql1) #查找该用户信息
    db=MysqlUtil() #实例化数据库操作类
    sql2="SELECT *FROM linkman where dormitory_id=%s"%(dormitory_id)
    result2=db.fetchall(sql2)
    if not result2: #如果未设定联系人
        result2=[{'linkman_name':'无','linkman_email':'无'}]
    #修改信息
    if request.method=='POST':#如果提交表单
        #获取字段内容
        num=int(request.form['num'])
        db=MysqlUtil() #实例化数据库操作类
        sql="UPDATE dormitory SET banlance=%d WHERE dormitory_id=%s"%(num,dormitory_id)#user表中插入记录
        db.insert(sql)
        flash('修改成功','success') #闪存信息
        return redirect(url_for('dashboard')) # 跳转到登录页面
    return render_template('dashboard_edit.html',dormitory=result1,linkman=result2)    #渲染模板

#退出登录
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('您已成功退出','success') #闪存信息
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key='f86618661'
    app.run(debug=True)
