from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from src.models import (
    Usuario, Profesional, Empresa,
    Publicacion, Comentario,
    Habilidad, Educacion, ExperienciaLaboral,
    OfertaEmpleo, Postulacion,
    Conversacion, Mensaje
)

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de demostración'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando población de datos...'))
        
        # Limpiar datos existentes (opcional)
        if input('¿Deseas limpiar datos existentes? (s/n): ').lower() == 's':
            self.limpiar_datos()
        
        # Crear usuarios
        self.crear_usuarios_admin()
        self.crear_usuarios_profesionales()
        self.crear_usuarios_empresas()
        
        # Crear contenido
        self.crear_publicaciones()
        self.crear_ofertas_laborales()
        self.crear_conversaciones()
        
        self.stdout.write(self.style.SUCCESS('✅ Datos de demostración creados exitosamente!'))
        self.mostrar_credenciales()
    
    def limpiar_datos(self):
        self.stdout.write('Limpiando datos existentes...')
        Usuario.objects.all().delete()
        self.stdout.write(self.style.WARNING('Datos limpiados'))
    
    def crear_usuarios_admin(self):
        self.stdout.write('Creando usuario administrador...')
        
        # Admin
        admin = Usuario.objects.create_superuser(
            username='admin@linkingx.com',
            email='admin@linkingx.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema',
            tipo_usuario='profesional'
        )
        
        Profesional.objects.create(
            user=admin,
            cedula='12345678',
            fecha_nacimiento='1990-01-01',
            genero='masculino',
            titulo_actual='Administrador del Sistema',
            descripcion_personal='Administrador del sistema Linking X'
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Admin creado'))
    
    def crear_usuarios_profesionales(self):
        self.stdout.write('Creando usuarios profesionales...')
        
        profesionales_data = [
            {
                'email': 'andreinacarolaineve@gmail.com',
                'password': 'demo123',
                'first_name': 'andreina',
                'last_name': 'velasquez',
                'ubicacion': 'Caracas, Venezuela',
                'cedula': '28309031',
                'fecha_nacimiento': '2000-03-15',
                'genero': 'femenino',
                'titulo_actual': 'Desarrolladora Full Stack',
                'descripcion_personal': 'Apasionada por crear soluciones tecnológicas innovadoras. 5 años de experiencia en desarrollo web con Python y React.',
                'linkedin_url': 'https://linkedin.com/in/andreina',
                'github_url': 'https://github.com/andreina',
                'habilidades': [
                    ('Python', 'avanzado'),
                    ('Django', 'avanzado'),
                    ('React', 'intermedio'),
                    ('PostgreSQL', 'avanzado'),
                    ('Git', 'avanzado'),
                ],
                'educacion': {
                    'institucion': 'Universidad Central de Venezuela',
                    'titulo': 'Ingeniería en Computación',
                    'campo_estudio': 'Ciencias de la Computación',
                    'fecha_inicio': '2023-09-01',
                    'fecha_fin': '2028-07-15',
                },
                'experiencia': {
                    'empresa': 'Tech Solutions CA',
                    'cargo': 'Desarrolladora Senior',
                    'tipo_empleo': 'tiempo_completo',
                    'modalidad': 'remoto',
                    'fecha_inicio': '2020-01-01',
                    'trabajo_actual': True,
                    'descripcion': 'Desarrollo de aplicaciones web empresariales utilizando Django y React.',
                }
            },
            {
                'email': 'nicole.llerena@gmail.com',
                'password': 'demo123',
                'first_name': 'nicole',
                'last_name': 'llerena',
                'ubicacion': 'Caracas, Venezuela',
                'cedula': '23456789',
                'fecha_nacimiento': '2001-03-21',
                'genero': 'femenino',
                'titulo_actual': 'Diseñador UX/UI',
                'descripcion_personal': 'Diseñador con enfoque en experiencia de usuario. Me encanta crear interfaces intuitivas y atractivas.',
                'linkedin_url': 'https://linkedin.com/in/nicovuxci',
                'habilidades': [
                    ('Figma', 'experto'),
                    ('Adobe XD', 'avanzado'),
                    ('UI Design', 'experto'),
                    ('Prototyping', 'avanzado'),
                ],
                'educacion': {
                    'institucion': 'Universidad Central de Venezuela',
                    'titulo': 'Diseño Gráfico',
                    'campo_estudio': 'Diseño',
                    'fecha_inicio': '2010-09-01',
                    'fecha_fin': '2016-07-15',
                },
                'experiencia': {
                    'empresa': 'Creative Agency',
                    'cargo': 'Lead UX Designer',
                    'tipo_empleo': 'tiempo_completo',
                    'modalidad': 'hibrido',
                    'fecha_inicio': '2018-06-01',
                    'trabajo_actual': True,
                    'descripcion': 'Liderazgo de equipo de diseño UX/UI para proyectos corporativos.',
                }
            },
            {
                'email': 'andreina.velasquez@gmail.com',
                'password': 'demo123',
                'first_name': 'andreina',
                'last_name': 'Velasquez',
                'ubicacion': 'Caracas, Venezuela',
                'cedula': '34567890',
                'fecha_nacimiento': '1998-11-10',
                'genero': 'femenino',
                'titulo_actual': 'Data Scientist',
                'descripcion_personal': 'Especialista en análisis de datos y machine learning. Busco oportunidades para aplicar IA en problemas reales.',
                'linkedin_url': 'https://linkedin.com/in/andreinavelasquez',
                'github_url': 'https://github.com/andreinavelasquez',
                'habilidades': [
                    ('Python', 'experto'),
                    ('Machine Learning', 'avanzado'),
                    ('TensorFlow', 'intermedio'),
                    ('Pandas', 'avanzado'),
                    ('SQL', 'avanzado'),
                ],
                'educacion': {
                    'institucion': 'Universidad de Carabobo',
                    'titulo': 'Ingeniería en Informática',
                    'campo_estudio': 'Informática',
                    'fecha_inicio': '2016-09-01',
                    'fecha_fin': '2021-07-15',
                },
                'experiencia': {
                    'empresa': 'DataCorp',
                    'cargo': 'Junior Data Scientist',
                    'tipo_empleo': 'tiempo_completo',
                    'modalidad': 'remoto',
                    'fecha_inicio': '2021-08-01',
                    'trabajo_actual': True,
                    'descripcion': 'Desarrollo de modelos predictivos para análisis de negocios.',
                }
            },
        ]
        
        for data in profesionales_data:
            # Crear usuario
            user = Usuario.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                ubicacion=data['ubicacion'],
                tipo_usuario='profesional'
            )
            
            # Crear perfil profesional
            profesional = Profesional.objects.create(
                user=user,
                cedula=data['cedula'],
                fecha_nacimiento=data['fecha_nacimiento'],
                genero=data['genero'],
                titulo_actual=data['titulo_actual'],
                descripcion_personal=data['descripcion_personal'],
                linkedin_url=data.get('linkedin_url', ''),
                github_url=data.get('github_url', ''),
            )
            
            # Crear habilidades
            for habilidad_nombre, nivel in data['habilidades']:
                Habilidad.objects.create(
                    profesional=profesional,
                    nombre=habilidad_nombre,
                    nivel=nivel
                )
            
            # Crear educación
            edu_data = data['educacion']
            Educacion.objects.create(
                profesional=profesional,
                institucion=edu_data['institucion'],
                titulo=edu_data['titulo'],
                campo_estudio=edu_data['campo_estudio'],
                fecha_inicio=edu_data['fecha_inicio'],
                fecha_fin=edu_data.get('fecha_fin'),
                en_curso=edu_data.get('fecha_fin') is None
            )
            
            # Crear experiencia
            exp_data = data['experiencia']
            ExperienciaLaboral.objects.create(
                profesional=profesional,
                empresa=exp_data['empresa'],
                cargo=exp_data['cargo'],
                tipo_empleo=exp_data['tipo_empleo'],
                modalidad=exp_data['modalidad'],
                fecha_inicio=exp_data['fecha_inicio'],
                trabajo_actual=exp_data['trabajo_actual'],
                descripcion=exp_data['descripcion']
            )
            
            self.stdout.write(f'✓ Profesional creado: {user.get_full_name()}')
    
    def crear_usuarios_empresas(self):
        self.stdout.write('Creando usuarios empresas...')
        
        empresas_data = [
            {
                'email': 'rh@techsolutions.com',
                'password': 'demo123',
                'nombre_empresa': 'Tech Solutions CA',
                'rif': 'J-123456789',
                'tipo_empresa': 'startup',
                'ubicacion': 'Caracas, Venezuela',
                'descripcion_breve': 'Startup de desarrollo de software',
                'descripcion_completa': 'Somos una startup venezolandreina enfocada en crear soluciones tecnológicas innovadoras. Buscamos talento apasionado por la tecnología.',
                'sector': 'Tecnología',
                'tamano': '11-50',
                'ano_fundacion': 2019,
                'sitio_web': 'https://techsolutions.com.ve',
                'telefono': '+58 212 1234567',
                'email_contacto': 'rh@techsolutions.com',
            },
            {
                'email': 'talento@innovatech.com',
                'password': 'demo123',
                'nombre_empresa': 'InnovaTech Corp',
                'rif': 'J-987654321',
                'tipo_empresa': 'corporacion',
                'ubicacion': 'Maracaibo, Venezuela',
                'descripcion_breve': 'Corporación líder en transformación digital',
                'descripcion_completa': 'Empresa líder en servicios de transformación digital y consultoría tecnológica con más de 15 años en el mercado.',
                'sector': 'Consultoría IT',
                'tamano': '51-200',
                'ano_fundacion': 2008,
                'sitio_web': 'https://innovatech.com',
                'telefono': '+58 261 7654321',
                'email_contacto': 'talento@innovatech.com',
            },
            {
                'email': 'contacto@dataanalytics.com',
                'password': 'demo123',
                'nombre_empresa': 'Data Analytics Venezuela',
                'rif': 'J-456789123',
                'tipo_empresa': 'pyme',
                'ubicacion': 'Valencia, Venezuela',
                'descripcion_breve': 'Especialistas en análisis de datos',
                'descripcion_completa': 'Ayudamos a empresas a tomar decisiones basadas en datos mediante análisis avanzados y soluciones de BI.',
                'sector': 'Data Science',
                'tamano': '11-50',
                'ano_fundacion': 2015,
                'sitio_web': 'https://dataanalitycs.com.ve',
                'telefono': '+58 241 9876543',
                'email_contacto': 'contacto@dataanalitycs.com',
            },
        ]
        
        for data in empresas_data:
            # Crear usuario
            user = Usuario.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['nombre_empresa'],
                ubicacion=data['ubicacion'],
                tipo_usuario='empresa'
            )
            
            # Crear perfil empresa
            Empresa.objects.create(
                user=user,
                nombre_empresa=data['nombre_empresa'],
                rif=data['rif'],
                tipo_empresa=data['tipo_empresa'],
                descripcion_breve=data['descripcion_breve'],
                descripcion_completa=data['descripcion_completa'],
                sector=data['sector'],
                tamano=data['tamano'],
                ano_fundacion=data['ano_fundacion'],
                sitio_web=data['sitio_web'],
                telefono=data['telefono'],
                email_contacto=data['email_contacto'],
            )
            
            self.stdout.write(f'✓ Empresa creada: {data["nombre_empresa"]}')
    
    def crear_publicaciones(self):
        self.stdout.write('Creando publicaciones...')
        
        usuarios = Usuario.objects.all()
        
        publicaciones_data = [
            {
                'contenido': '¡Acabo de terminar un proyecto increíble con Django y React! 🚀 Las posibilidades son infinitas cuando combinas estas tecnologías. ¿Alguien más trabajando con este stack?',
                'usuario': 'andreina.ve@gmail.com',
            },
            {
                'contenido': '¿Buscan un diseñador UX/UI? Estoy disponible para proyectos freelance. Mi enfoque es crear experiencias digitales memorables centradas en el usuario. 💡',
                'usuario': 'nicole.llerena@gmail.com',
            },
            {
                'contenido': 'Tech Solutions está creciendo y buscamos desarrolladores Python! Si te apasiona la tecnología y quieres formar parte de un equipo dinámico, esta es tu oportunidad. 👨‍💻👩‍💻',
                'usuario': 'rh@techsolutions.com',
            },
            {
                'contenido': 'Acabo de completar un curso de Machine Learning en Coursera. Los modelos predictivos son fascinantes. ¿Recomendaciones de proyectos para practicar? 📊🤖',
                'usuario': 'andreina.velasquez@gmail.com',
            },
            {
                'contenido': 'El trabajo remoto ha cambiado mi vida profesional. Mayor productividad, mejor balance vida-trabajo, y más tiempo con mi familia. ¿Cuál ha sido su experiencia? 🏠💼',
                'usuario': 'andreina.ve@gmail.com',
            },
            {
                'contenido': 'InnovaTech está buscando talento senior para liderar proyectos de transformación digital. Si tienes experiencia en arquitectura de software y liderazgo de equipos, contáctanos. 🎯',
                'usuario': 'talento@innovatech.com',
            },
            {
                'contenido': 'El diseño no es solo cómo se ve, es cómo funciona. Steve Jobs tenía razón. Cada pixel importa, cada interacción cuenta. 🎨✨',
                'usuario': 'nicole.llerena@gmail.com',
            },
            {
                'contenido': '¿Sabían que Python sigue siendo el lenguaje #1 para Data Science? Su ecosistema de librerías es incomparable: Pandas, NumPy, Scikit-learn, TensorFlow... 🐍📈',
                'usuario': 'andreina.velasquez@gmail.com',
            },
        ]
        
        for pub_data in publicaciones_data:
            try:
                user = Usuario.objects.get(email=pub_data['usuario'])
                pub = Publicacion.objects.create(
                    creador=user,
                    contenido=pub_data['contenido'],
                    likes_count=0
                )
                # Ajustar fecha para variedad
                dias_atras = publicaciones_data.index(pub_data)
                pub.fecha = timezone.now() - timedelta(days=dias_atras)
                pub.save()
            except Usuario.DoesNotExist:
                continue
        
        # Crear algunos comentarios
        publicaciones = Publicacion.objects.all()
        if publicaciones.exists():
            pub1 = publicaciones.first()
            user_comentario = Usuario.objects.exclude(email=pub1.creador.email).first()
            
            Comentario.objects.create(
                publicacion=pub1,
                creador=user_comentario,
                contenido='¡Excelente! Yo también trabajo con ese stack. ¿Usaste Redux para el state mandreinagement?'
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ {publicaciones.count()} publicaciones creadas'))
    
    def crear_ofertas_laborales(self):
        self.stdout.write('Creando ofertas laborales...')
        
        ofertas_data = [
            {
                'empresa_email': 'rh@techsolutions.com',
                'titulo': 'Desarrollador Python Senior',
                'descripcion': '''Buscamos un desarrollador Python senior con experiencia en Django para unirse a nuestro equipo de desarrollo.

Responsabilidades:
- Desarrollo de aplicaciones web con Django
- Diseño de APIs RESTful
- Optimización de bases de datos
- Code reviews y mentoría de desarrolladores junior
- Trabajo en equipo ágil (Scrum)''',
                'requisitos': '''Experiencia mínima de 5 años en desarrollo Python
Dominio avanzado de Django y Django REST Framework
Experiencia con PostgreSQL
Conocimientos de Git y metodologías ágiles
Inglés intermedio (lectura técnica)''',
                'responsabilidades': 'Liderar el desarrollo de nuevas funcionalidades, mantener código legacy, optimizar performance.',
                'nivel': 'senior',
                'tipo_empleo': 'tiempo_completo',
                'modalidad': 'remoto',
                'ubicacion': 'Caracas, Venezuela (Remoto)',
                'salario_min': 2000,
                'salario_max': 3500,
                'mostrar_salario': True,
                'destacada': True,
            },
            {
                'empresa_email': 'rh@techsolutions.com',
                'titulo': 'Diseñador UX/UI',
                'descripcion': '''Estamos en búsqueda de un diseñador UX/UI creativo y con ojo para el detalle que nos ayude a crear experiencias digitales excepcionales.

Trabajarás directamente con el equipo de producto para diseñar interfaces intuitivas y atractivas.''',
                'requisitos': '''Experiencia de 3+ años en diseño UX/UI
Portfolio demostrable
Dominio de Figma
Conocimientos de Adobe XD
Experiencia en design systems''',
                'responsabilidades': 'Crear wireframes y prototipos, realizar pruebas de usabilidad, mantener el design system.',
                'nivel': 'mid',
                'tipo_empleo': 'tiempo_completo',
                'modalidad': 'hibrido',
                'ubicacion': 'Caracas, Venezuela',
                'salario_min': 1500,
                'salario_max': 2500,
                'mostrar_salario': True,
                'destacada': True,
            },
            {
                'empresa_email': 'talento@innovatech.com',
                'titulo': 'Arquitecto de Software',
                'descripcion': '''InnovaTech busca un Arquitecto de Software para liderar la definición de arquitecturas tecnológicas en proyectos de transformación digital.

Serás responsable de diseñar soluciones escalables y robustas para nuestros clientes corporativos.''',
                'requisitos': '''10+ años de experiencia en desarrollo de software
5+ años en roles de arquitectura
Conocimientos profundos de microservicios
Experiencia con cloud (AWS, Azure, GCP)
Liderazgo técnico comprobado''',
                'responsabilidades': 'Diseñar arquitecturas de soluciones, liderar equipos técnicos, definir estándares tecnológicos.',
                'nivel': 'lead',
                'tipo_empleo': 'tiempo_completo',
                'modalidad': 'hibrido',
                'ubicacion': 'Maracaibo, Venezuela',
                'salario_min': 4000,
                'salario_max': 6000,
                'mostrar_salario': False,
                'destacada': True,
            },
            {
                'empresa_email': 'contacto@dataanalitycs.com',
                'titulo': 'Data Scientist Junior',
                'descripcion': '''Data analitycs Venezuela está creciendo y buscamos un Data Scientist Junior apasionado por los datos y el machine learning.

Es una excelente oportunidad para crecer profesionalmente en un ambiente dinámico.''',
                'requisitos': '''Título en Ingeniería, Matemáticas, Estadística o afín
Conocimientos de Python (Pandas, NumPy, Scikit-learn)
Conocimientos básicos de SQL
Experiencia con visualización de datos
Gandreinas de aprender''',
                'responsabilidades': 'Análisis exploratorio de datos, crear dashboards, entrenar modelos predictivos, presentar insights.',
                'nivel': 'junior',
                'tipo_empleo': 'tiempo_completo',
                'modalidad': 'remoto',
                'ubicacion': 'Valencia, Venezuela (Remoto)',
                'salario_min': 1000,
                'salario_max': 1800,
                'mostrar_salario': True,
                'destacada': False,
            },
            {
                'empresa_email': 'talento@innovatech.com',
                'titulo': 'Frontend Developer React',
                'descripcion': '''Buscamos un Frontend Developer con sólidos conocimientos en React para desarrollar interfaces modernas y responsive.''',
                'requisitos': '''3+ años de experiencia con React
Dominio de JavaScript/TypeScript
Experiencia con Redux o Context API
Conocimientos de CSS/SASS
Git y metodologías ágiles''',
                'responsabilidades': 'Desarrollar componentes React, integrar con APIs REST, optimizar performance frontend.',
                'nivel': 'mid',
                'tipo_empleo': 'tiempo_completo',
                'modalidad': 'remoto',
                'ubicacion': 'Venezuela (Remoto)',
                'salario_min': 1800,
                'salario_max': 2800,
                'mostrar_salario': True,
                'destacada': False,
            },
            {
                'empresa_email': 'rh@techsolutions.com',
                'titulo': 'Pasante de Desarrollo Web',
                'descripcion': '''Oportunidad de pasantía para estudiantes de Ingeniería en Computación o Informática que quieran gandreinar experiencia real en desarrollo web.''',
                'requisitos': '''Estudiante activo de Ingeniería
Conocimientos básicos de HTML, CSS, JavaScript
Conocimientos de Python (deseable)
Disponibilidad de 6 meses
Proactividad y gandreinas de aprender''',
                'responsabilidades': 'Apoyar en desarrollo de features, realizar pruebas, documentar código, aprender tecnologías.',
                'nivel': 'junior',
                'tipo_empleo': 'pasantia',
                'modalidad': 'hibrido',
                'ubicacion': 'Caracas, Venezuela',
                'salario_min': 300,
                'salario_max': 500,
                'mostrar_salario': True,
                'destacada': False,
            },
        ]
        
        for oferta_data in ofertas_data:
            try:
                empresa_user = Usuario.objects.get(email=oferta_data['empresa_email'])
                empresa = empresa_user.empresa
                
                oferta = OfertaEmpleo.objects.create(
                    empresa=empresa,
                    titulo=oferta_data['titulo'],
                    descripcion=oferta_data['descripcion'],
                    requisitos=oferta_data['requisitos'],
                    responsabilidades=oferta_data['responsabilidades'],
                    nivel=oferta_data['nivel'],
                    tipo_empleo=oferta_data['tipo_empleo'],
                    modalidad=oferta_data['modalidad'],
                    ubicacion=oferta_data['ubicacion'],
                    salario_min=oferta_data['salario_min'],
                    salario_max=oferta_data['salario_max'],
                    mostrar_salario=oferta_data['mostrar_salario'],
                    activa=True,
                    destacada=oferta_data['destacada'],
                    vistas=0
                )
                
                # Ajustar fecha
                dias_atras = ofertas_data.index(oferta_data)
                oferta.fecha_publicacion = timezone.now() - timedelta(days=dias_atras)
                oferta.save()
                
            except (Usuario.DoesNotExist, Empresa.DoesNotExist):
                continue
        
        ofertas_count = OfertaEmpleo.objects.count()
        self.stdout.write(self.style.SUCCESS(f'✓ {ofertas_count} ofertas laborales creadas'))
    
    def crear_conversaciones(self):
        self.stdout.write('Creando conversaciones de prueba...')
        
        try:
            # Conversación entre profesionales
            andreina = Usuario.objects.get(email='andreina.ve@gmail.com')
            nicole = Usuario.objects.get(email='nicole.llerena@gmail.com')
            
            conv1 = Conversacion.objects.create(
                participante_1=andreina,
                participante_2=nicole
            )
            
            Mensaje.objects.create(
                conversacion=conv1,
                emisor=andreina,
                receptor=nicole,
                contenido='¡Hola nicole! Vi tu trabajo en Behance, está increíble. ¿Tienes tiempo para colaborar en un proyecto?',
                fecha_envio=timezone.now() - timedelta(hours=5)
            )
            
            Mensaje.objects.create(
                conversacion=conv1,
                emisor=nicole,
                receptor=andreina,
                contenido='¡Hola María! Muchas gracias. Claro que sí, cuéntame más sobre el proyecto.',
                leido=True,
                fecha_lectura=timezone.now() - timedelta(hours=4, minutes=45),
                fecha_envio=timezone.now() - timedelta(hours=4, minutes=45)
            )
            
            Mensaje.objects.create(
                conversacion=conv1,
                emisor=andreina,
                receptor=nicole,
                contenido='Es una aplicación web para gestión de proyectos. Necesitamos un diseño moderno y funcional.',
                fecha_envio=timezone.now() - timedelta(hours=2)
            )
            
            # Conversación entre profesional y empresa
            andreina = Usuario.objects.get(email='andreina.velasquez@gmail.com')
            empresa = Usuario.objects.get(email='contacto@dataanalitycs.com')
            
            conv2 = Conversacion.objects.create(
                participante_1=andreina,
                participante_2=empresa
            )
            
            Mensaje.objects.create(
                conversacion=conv2,
                emisor=andreina,
                receptor=empresa,
                contenido='Buenos días, estoy interesada en la posición de Data Scientist Junior que publicaron.',
                fecha_envio=timezone.now() - timedelta(days=1)
            )
            
            Mensaje.objects.create(
                conversacion=conv2,
                emisor=empresa,
                receptor=andreina,
                contenido='¡Hola andreina! Gracias por tu interés. ¿Tienes experiencia previa con machine learning?',
                leido=True,
                fecha_lectura=timezone.now() - timedelta(hours=20),
                fecha_envio=timezone.now() - timedelta(hours=20)
            )
            
            self.stdout.write(self.style.SUCCESS('✓ Conversaciones creadas'))
            
        except Usuario.DoesNotExist:
            self.stdout.write(self.style.WARNING('⚠ No se pudieron crear todas las conversaciones'))
    
    def mostrar_credenciales(self):
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('CREDENCIALES DE ACCESO'))
        self.stdout.write('='*60 + '\n')
        
        self.stdout.write(self.style.WARNING('ADMINISTRADOR:'))
        self.stdout.write('Email: admin@linkingx.com')
        self.stdout.write('Password: admin123\n')
        
        self.stdout.write(self.style.WARNING('PROFESIONALES:'))
        self.stdout.write('Email: andreina.ve@gmail.com | Password: demo123')
        self.stdout.write('Email: nicole.llerena@gmail.com | Password: demo123')
        self.stdout.write('Email: andreina.velasquez@gmail.com | Password: demo123\n')
        
        self.stdout.write(self.style.WARNING('EMPRESAS:'))
        self.stdout.write('Email: rh@techsolutions.com | Password: demo123')
        self.stdout.write('Email: talento@innovatech.com | Password: demo123')
        self.stdout.write('Email: contacto@dataanalitycs.com | Password: demo123\n')
        
        self.stdout.write('='*60 + '\n')