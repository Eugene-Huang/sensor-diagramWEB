import json
from app.models import User, Role

admin_list = []
student_list = []
teacher_list = []
users = User.query.all()
for u in users:
    role = Role.query.filter(u.role_id == Role.id).first().name
    if role == "Admin":
        admin_list.append(role)
    if role == "Student":
        student_list.append(role)
    if role == "Teacher":
        teacher_list.append(role)
admin_length = float(len(admin_list))
student_length = float(len(student_list))
teacher_length = float(len(teacher_list))
total = admin_length + student_length + teacher_length
admin_percent = (admin_length / total) * 100
student_percent = (student_length / total) * 100
teacher_percent = (teacher_length / total) * 100

chart_data = [["Admin", admin_percent], ["Student",
                                         student_percent], ["Teacher", teacher_percent]]
print json.dumps(chart_data)
