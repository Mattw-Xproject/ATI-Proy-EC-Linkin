from django.urls import path
from .views import (
    auth_login,
    auth_logout,
    auth_register_role,
    auth_register_profesional,
    auth_register_empresa,
    feed_home,
    profile_detail,
    profile_edit,
    profile_add_skill,
    profile_add_education,
    profile_add_experience,
    job_list,
    job_detail,
    job_apply,
    message_list,
    message_detail,
    add_section,
)

urlpatterns = [
    # Authentication
    path('login/', auth_login.login_view, name='auth_login'),
    path('logout/', auth_logout.logout_view, name='auth_logout'),
    path('register/', auth_register_role.register_role_view, name='auth_register_role'),
    path('register/profesional/', auth_register_profesional.register_profesional_view, name='auth_register_profesional'),
    path('register/empresa/', auth_register_empresa.register_empresa_view, name='auth_register_empresa'),
    
    # Core
    path('', feed_home, name='feed_home'),
    
    # Profile - Detail & Edit
    path('profile/<int:user_id>/', profile_detail.profile_detail, name='profile_detail'),
    path('profile/<int:user_id>/edit/', profile_edit.profile_edit, name='profile_edit'),
    
    # Profile - Skills
    path('profile/<int:user_id>/skills/add/', profile_add_skill.add_skill, name='add_skill'),
    path('profile/<int:user_id>/skills/<int:skill_id>/delete/', profile_add_skill.delete_skill, name='delete_skill'),
    
    # Profile - Education
    path('profile/<int:user_id>/education/add/', profile_add_education.add_education, name='add_education'),
    path('profile/<int:user_id>/education/<int:education_id>/edit/', profile_add_education.edit_education, name='edit_education'),
    path('profile/<int:user_id>/education/<int:education_id>/delete/', profile_add_education.delete_education, name='delete_education'),
    
    # Profile - Experience
    path('profile/<int:user_id>/experience/add/', profile_add_experience.add_experience, name='add_experience'),
    path('profile/<int:user_id>/experience/<int:experience_id>/edit/', profile_add_experience.edit_experience, name='edit_experience'),
    path('profile/<int:user_id>/experience/<int:experience_id>/delete/', profile_add_experience.delete_experience, name='delete_experience'),
    
    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/', job_detail.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', job_apply.job_apply, name='job_apply'),
    path('jobs/<int:job_id>/save/', job_apply.job_save, name='job_save'),
    # Messages
    path('messages/', message_list.message_list, name='message_list'),
    path('messages/<int:conversation_id>/', message_detail.message_detail, name='message_detail'),
    path('messages/<int:conversation_id>/send/', message_detail.send_message, name='send_message'),
    path('messages/new/<int:user_id>/', message_detail.create_conversation, name='create_conversation'),
    # Section Management
    path('profile/section/add/<str:section_type>/', add_section.add_section, name='add_section'),
    path('profile/section/edit/<str:section_type>/<int:section_id>/', add_section.edit_section, name='edit_section'),
    path('profile/section/delete/<str:section_type>/<int:section_id>/', add_section.delete_section, name='delete_section'),
]