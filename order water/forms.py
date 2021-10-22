from wtforms import Form, StringField, TextAreaField, PasswordField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class Linkman_Form(Form):
    linkman_name = StringField(
        '联系人姓名'
    )
    linkman_email= StringField(
        '联系人邮箱',
        validators = [
            DataRequired(message="请输入邮箱"),
            Email(message='请输入正确的邮箱格式')
        ]
    )

class Dormitory_Form(Form):
    school_name=SelectField(
        '学校名称',
        choices=[(1,'中央民族大学'),(2,'**大学')],
        validators=[DataRequired(message='请输入房间号')],
        coerce=int)
    dormitory_number=SelectField(
        '宿舍楼号',
        choices=[(1,'6号楼'),(2,'7号楼')],
        validators=[DataRequired(message='请输入房间号')],
        coerce=int)
    room_number=StringField(
        '房间号',
        validators=[
            DataRequired(message='请输入房间号')
        ]
    )
    email= StringField(
        '邮箱',
        validators = [
            DataRequired(message="请输入邮箱"),
            Email(message='请输入正确的邮箱格式')
        ]
    )
    password = PasswordField(
        '密码',
        validators = [
            DataRequired(message='密码不能为空'),
            Length(min=6,max=20,message='长度在6-20个字符之间'),
        ]
    )
    confirm = PasswordField(
        '确认密码',
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=6, max=20),
            EqualTo('password', message='2次输入密码不一致')
        ]
    )
    
class Order_Form(Form):
    order_date=SelectField(
        '送达日期',
        validators=[DataRequired(message='请选择送达日期')],
        coerce=int)
    order_time=SelectField(
        '送达时间',
        choices=[(1,'中午12点'),(2,'下午6点')],
        validators=[DataRequired(message='请选择送达时间')],
        coerce=int)
    water_brand=SelectField(
        '水的品牌',
        choices=[(1,'娃哈哈'),(2,'国星'),(3,'水状元')],
        validators=[DataRequired(message='请选择水的品牌')],
        coerce=int)
    water_number=SelectField(
        '水的数量',
        choices=[(1,'1桶'),(2,'2桶')],
        validators=[DataRequired(message='请选择水的数量')],
        coerce=int)


