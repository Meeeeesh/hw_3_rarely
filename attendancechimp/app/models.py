from django.db import models
from django.contrib.auth.models import User
 
 
class InstructorProfile(models.Model):
    """One Instructor may teach multiple Courses.
 
    Fields:
        instructor_id: ID number (primary key).
        name: Full name.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instructor_id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=50)
 
    def __str__(self):
        return self.name
 
 
class StudentProfile(models.Model):
    """One Student may enroll in multiple Courses and upload many QR codes.
 
    Fields:
        student_id: ID number (primary key).
        name: Full name.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=50)
 
    def __str__(self):
        return self.name
 
 
class Course(models.Model):
    """A Course taught by one Instructor.
 
    Relationship: many Courses for one InstructorProfile (foreign key).
    If the Instructor is deleted, Course is kept and instructor set to NULL.
 
    Fields:
        id: auto-incrementing primary key
        name: Name of the course.
        instructor: The Instructor who teaches the course (id).
        meeting_days: Days the course meets, e.g. "MWF" or "TTh".
        meeting_time: Time the course starts.
    """
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.SET_NULL, null=True)
    meeting_days = models.CharField(max_length=15)
    meeting_time = models.TimeField()
 
    def __str__(self):
        return self.name
 
 
class Enrollment(models.Model):
    """Links one Student to one Course.
 
    Relationship: Students to Courses is many-to-many, so this table holds
    one row per (student, course) pair.
    If the Student or the Course is deleted, the Enrollment is deleted too.
 
    Fields:
        id:      auto-incrementing primary key.
        student: The enrolled Student.
        course:  The Course they are enrolled in.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
 
    def __str__(self):
        return f"{self.student} in {self.course}"
 
 
class Lecture(models.Model):
    """Relationship: many Lectures for one Course (foreign key).
    If the Course is deleted, its Lectures are deleted too.
 
    Fields:
        id: Added automatically by Django (auto-incrementing primary key).
        course: The Course this lecture belongs to.
        date: The date of the lecture.
        qr_code: Unique identifier shown as a QR code in class.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    qr_code = models.CharField(max_length=100, unique=True)
 
    def __str__(self):
        return f"{self.course} on {self.date}"
 
 
class QRCodeUpload(models.Model):
    """A QR code to prove attendance.
 
    Relationship: many uploads for one StudentProfile (foreign key).
    If the Lecture is deleted, upload kept and lecture set to NULL.
 
    Fields:
        id:          auto-incrementing primary key.
        student:     The Student who uploaded the photo.
        lecture:     The Lecture the QR code belongs to.
        image:       The uploaded photo.
        uploaded_at: Date and time of the upload.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
 
    def is_matched(self):
        """Return True if this upload is linked to a Lecture."""
        return self.lecture is not None
 
    def __str__(self):
        return f"Upload {self.id} by {self.student}"
