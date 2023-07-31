from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:saran@localhost/checks'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AnnouncementModel(db.Model):
    __tablename__ = "announcement"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    attachments = db.Column(db.String(120), nullable=False)

    announcement_topic_id = db.Column(db.Integer, db.ForeignKey("announcementtopic.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    teams_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    author = db.relationship('EmployeeModel', foreign_keys=[author_id])
    employee = db.relationship('EmployeeModel', foreign_keys=[employee_id])

    def __repr__(self):
        return f"{self.title}"


class AnnouncementTopicModel(db.Model):
    __tablename__ = "announcementtopic"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_to_everyone = db.Column(db.Boolean, nullable=False)

    announcements = db.relationship("AnnouncementModel", backref="topic", lazy=True)

    def __repr__(self):
        return f"{self.topic}"


class AssetCategoryModel(db.Model):
    __tablename__ = "assetcategory"

    id = db.Column(db.Integer, primary_key=True)
    asset_category_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    assets = db.relationship("AssetsModel", backref="asset_category", lazy=True)

    def __repr__(self):
        return f"{self.asset_category_name}"


class AssetsModel(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    asset_number = db.Column(db.String(120), nullable=False)
    serial_number = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(120), nullable=False)

    asset_category_id = db.Column(db.Integer, db.ForeignKey("assetcategory.id"), nullable=False)

    def __repr__(self):
        return f"{self.asset_name}"


class ClientModel(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(120), nullable=False)
    client_short_name = db.Column(db.String(120), nullable=False)
    contact_manager = db.Column(db.String(120), nullable=False)
    contact_mail = db.Column(db.String(120), nullable=False, unique=True)
    contact_phone_number = db.Column(db.String(120), nullable=False, unique=True)
    contact_address = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    projects = db.relationship('ProjectsModel', backref='client', lazy=True)
    teams = db.relationship('TeamsModel', backref='client', lazy=True)
    employees = db.relationship("EmployeeModel", backref="client", lazy=True)
    leave_policies = db.relationship("LeavePolicyModel", backref="client", lazy=True)
    announcements = db.relationship("AnnouncementModel", backref="client", lazy=True)

    def __repr__(self):
        return f"{self.client_name}"


class CompanyModel(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    short_title = db.Column(db.String(120), nullable=False)
    logo = db.Column(db.String(120), nullable=False, default="image.jpg")
    contact_number = db.Column(db.String(120), nullable=False, unique=True)
    address_1 = db.Column(db.String(120), nullable=False)
    address_2 = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    zip_code = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    status = db.Column(db.String(120), nullable=False)

    clients = db.relationship('ClientModel', backref='company', lazy=True)
    teams = db.relationship('TeamsModel', backref='company', lazy=True)
    employees = db.relationship("EmployeeModel", backref="company", lazy=True)
    leave_policies = db.relationship("LeavePolicyModel", backref="company", lazy=True)
    announcements = db.relationship("AnnouncementModel", backref="company", lazy=True)

    def __repr__(self):
        return f"{self.company_name}"


class EmergencyContactInfoModel(db.Model):
    __tablename__ = "emergencycontactinfo"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    relationship = db.Column(db.String(120), nullable=False)
    home_phone = db.Column(db.String(120), nullable=False, unique=True)
    mobile_phone = db.Column(db.String(120), nullable=False, unique=True)
    work_phone = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    country = db.Column(db.String(120), nullable=False)
    address_1 = db.Column(db.String(120), nullable=False)
    address_2 = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    zip_code = db.Column(db.String(120), nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    def __repr__(self):
        return f"{self.fullname}"


employeeposition_employee = db.Table("employeeposition_employee",
                                     db.Column("employeeposition_id", db.Integer, db.ForeignKey("employeeposition.id"),
                                               nullable=False),
                                     db.Column("employee_id", db.Integer, db.ForeignKey("employee.id"), nullable=False))


class EmployeePositionModel(db.Model):
    __tablename__ = "employeeposition"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    current_active = db.Column(db.Boolean, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    employees = db.relationship("EmployeeModel", secondary=employeeposition_employee, lazy=True, backref="position")

    employee_role_policy_id = db.Column(db.Integer, db.ForeignKey("employeerolepolicy.id"), nullable=False)

    def __repr__(self):
        return f"{self.id}"


class EmployeeModel(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    middle_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    work_email = db.Column(db.String(120), nullable=False, unique=True)
    work_phone = db.Column(db.String(120), nullable=False, unique=True)
    work_location = db.Column(db.String(120), nullable=False)
    employment_start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    employment_status = db.Column(db.String(120), nullable=False)
    employee_number = db.Column(db.String(120), nullable=False)
    skills = db.Column(db.String(120), nullable=False)

    emergency_contact_infos = db.relationship("EmergencyContactInfoModel", backref="employee", lazy=True)
    employee_bank_details = db.relationship("EmployeeBankDetailModel", backref="employee", lazy=True)
    employee_passports = db.relationship("EmployeePassportModel", backref="employee", lazy=True)
    employee_visas = db.relationship("EmployeeVisaModel", backref="employee", lazy=True)
    employee_educations = db.relationship("EmployeeEducationModel", backref="employee", lazy=True)
    employee_certifications = db.relationship("EmployeeCertificationModel", backref="employee", lazy=True)
    leave_policies = db.relationship("LeavePolicyModel", backref="employee", lazy=True)
    leave_employees = db.relationship("LeaveEmployeeModel", backref="employee", lazy=True)

    employee_personal_info_id = db.Column(db.Integer, db.ForeignKey("employeepersonalinfo.id", ondelete="CASCADE"),unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    projects_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    teams_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    onboarding_mentor_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    direct_manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    onboarding_mentor = db.relationship('EmployeeModel', remote_side=[id], backref='employee', lazy=True, foreign_keys=[onboarding_mentor_id])
    direct_manager = db.relationship('EmployeeModel', remote_side=[id], backref='employees', lazy=True, foreign_keys=[direct_manager_id])

    def __repr__(self):
        return f"{self.first_name}"


class EmployeeBankDetailModel(db.Model):
    __tablename__ = "employeebankdetail"

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(120), nullable=False, unique=True)
    sort_code = db.Column(db.String(120), nullable=False)
    bank_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    primary_account = db.Column(db.Boolean, nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    def __repr__(self):
        return f"{self.account_number}"


class EmployeeCertificationModel(db.Model):
    __tablename__ = "employeecertification"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    institution = db.Column(db.String(120), nullable=False)
    issued_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(120), nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    def __repr__(self):
        return f"{self.name}"


class EmployeeEducationModel(db.Model):
    __tablename__ = "employeeeducation"

    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(120), nullable=False)
    institution = db.Column(db.String(120), nullable=False)
    major = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    grade = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(120), nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    def __repr__(self):
        return f"{self.degree}"


class EmployeePassportModel(db.Model):
    __tablename__ = "employeepassport"

    id = db.Column(db.Integer, primary_key=True)
    passport_number = db.Column(db.String(120), nullable=False, unique=True)
    country_of_issue = db.Column(db.String(120), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    issuing_authority = db.Column(db.String(120), nullable=False)
    place_of_birth = db.Column(db.DateTime, nullable=False)
    nationality = db.Column(db.String(120), nullable=False)
    attachment = db.Column(db.String(120), nullable=False)
    current_active = db.Column(db.Boolean, nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    def __repr__(self):
        return f"{self.passport_number}"


class EmployeePersonalInfoModel(db.Model):
    __tablename__ = "employeepersonalinfo"

    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    address_1 = db.Column(db.String(120), nullable=False)
    address_2 = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    zip_code = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    nationality = db.Column(db.String(120), nullable=False)
    home_phone = db.Column(db.String(120), nullable=False, unique=True)
    mobile_phone = db.Column(db.String(120), nullable=False, unique=True)
    personal_email = db.Column(db.String(120), nullable=False, unique=True)
    gender = db.Column(db.String(120), nullable=False)
    marital_state = db.Column(db.String(120), nullable=False)

    employeess = db.relationship("EmployeeModel", backref="employee_personal_info", uselist=False, lazy=True)

    def __repr__(self):
        return f"{self.date_of_birth}"


class EmployeeRolePolicyModel(db.Model):
    __tablename__ = "employeerolepolicy"

    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(120), nullable=False)
    position_code = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    employee_positions = db.relationship("EmployeePositionModel", backref="position_name", lazy=True)

    def __repr__(self):
        return f"{self.position_name}"


class EmployeeVisaModel(db.Model):
    __tablename__ = "employeevisa"

    id = db.Column(db.Integer, primary_key=True)
    visa_number = db.Column(db.String(120), nullable=False, unique=True)
    visa_type = db.Column(db.String(120), nullable=False)
    country_of_issue = db.Column(db.String(120), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    issue_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    issuing_authority = db.Column(db.String(120), nullable=False)
    purpose_of_travel = db.Column(db.String(120), nullable=False)
    remarks = db.Column(db.String(120), nullable=False)
    attachment = db.Column(db.String(120), nullable=False)
    current_active = db.Column(db.Boolean, nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    def __repr__(self):
        return f"{self.visa_number}"


class LeaveAllocationModel(db.Model):
    __tablename__ = "leaveallocation"

    id = db.Column(db.Integer, primary_key=True)
    policy_allocation_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    leave_policies = db.relationship("LeavePolicyModel", backref="allocated_type", lazy=True)

    def __repr__(self):
        return f"{self.policy_allocation_name}"


class LeaveEmployeeModel(db.Model):
    __tablename__ = "leaveemployee"

    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    number_of_days = db.Column(db.Integer, nullable=False)
    approved_status = db.Column(db.String(120), nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    leave_policy_id = db.Column(db.Integer, db.ForeignKey("leavepolicy.id"), nullable=False)

    def __repr__(self):
        return f"{self.reason}"


class LeavePolicyModel(db.Model):
    __tablename__ = "leavepolicy"

    id = db.Column(db.Integer, primary_key=True)
    policy_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    allocated_days = db.Column(db.Integer, nullable=False)
    working_hours = db.Column(db.Integer, nullable=False)
    do_carry_over = db.Column(db.Boolean, nullable=False)
    is_show_in_employee_calender = db.Column(db.Boolean, nullable=False)

    leave_employees = db.relationship("LeaveEmployeeModel", backref="leavepolicy", lazy=True)

    leave_allocation_id = db.Column(db.Integer, db.ForeignKey("leaveallocation.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    def __repr__(self):
        return f"{self.policy_name}"


class PayslipsModel(db.Model):
    __tablename__ = "payslips"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_hours = db.Column(db.Integer, nullable=False)
    number_of_days = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.String(120), nullable=False)
    attachment = db.Column(db.String(120), nullable=False)

    resource_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    resource = db.relationship('EmployeeModel', foreign_keys=[resource_id])
    reporter = db.relationship('EmployeeModel', foreign_keys=[reporter_id])



    def __repr__(self):
        return f"{self.status}"


class ProjectsModel(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(120), nullable=False, unique=True)
    project_short_name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(120), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    teams = db.relationship('TeamsModel', backref='project', lazy=True)
    employees = db.relationship("EmployeeModel", backref="project", lazy=True)
    time_sheets = db.relationship("TimeSheetModel", backref="project", lazy=True)
    announcements = db.relationship("AnnouncementModel", backref="project", lazy=True)

    def __repr__(self):
        return f"{self.project_name}"


class TaskModel(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    task_status = db.Column(db.String(120), nullable=False)
    original_estimate = db.Column(db.Integer, nullable=False)

    task_priority_id = db.Column(db.Integer, db.ForeignKey("taskpriority.id"), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    assignee = db.relationship('EmployeeModel', foreign_keys=[assignee_id])
    reporter = db.relationship('EmployeeModel', foreign_keys=[reporter_id])



    def __repr__(self):
        return f"{self.title}"


class TaskPriorityModel(db.Model):
    __tablename__ = "taskpriority"

    id = db.Column(db.Integer, primary_key=True)
    priority_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority_range = db.Column(db.Integer, nullable=False)

    tasks = db.relationship("TaskModel", backref="priority", lazy=True)

    def __repr__(self):
        return f"{self.priority_name}"


class TeamsModel(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(120), nullable=False, unique=True)
    team_short_name = db.Column(db.String(120), nullable=False, unique=True)
    team_manager = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    employees = db.relationship("EmployeeModel", backref="team", lazy=True)
    announcements = db.relationship("AnnouncementModel", backref="team", lazy=True)

    def __repr__(self):
        return f"{self.team_name}"


class TimeSheetModel(db.Model):
    __tablename__ = "timesheet"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(120), nullable=False)
    total_hours = db.Column(db.Integer, nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    resource = db.relationship('EmployeeModel', foreign_keys=[resource_id])
    reporter = db.relationship('EmployeeModel', foreign_keys=[reporter_id])

    def __repr__(self):
        return f"{self.date}"


if __name__ == "__main__":
    app.run(debug=True)
