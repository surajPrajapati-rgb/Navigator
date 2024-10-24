from django.core.management.base import BaseCommand
from faker import Faker
from mentorship.models import (
    Mentor, MentorSkill, MentorCategory, MentorAvailability,
    Review, Message, Session, Payment
)
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils import timezone
import random
import string
from datetime import time, timedelta

class Command(BaseCommand):
    help = 'Generate fake data for all models in the mentorship system'

    def generate_unique_username(self, fake):
        username = fake.user_name()
        while User.objects.filter(username=username).exists():
            username = f"{fake.user_name()}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=5))}"
        return username

    def create_mentor_availability(self, fake, mentor):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for day in random.sample(days, random.randint(2, 5)):
            start_hour = random.randint(9, 16)
            end_hour = start_hour + random.randint(2, 4)
            MentorAvailability.objects.create(
                mentor=mentor,
                day_of_week=day,
                start_time=time(start_hour, 0),
                end_time=time(end_hour, 0)
            )

    def create_messages(self, fake, mentor_user, mentee_user):
        for _ in range(random.randint(1, 5)):
            Message.objects.create(
                sender=random.choice([mentor_user, mentee_user]),
                receiver=mentee_user if random.choice([mentor_user, mentee_user]) == mentor_user else mentor_user,
                content=fake.paragraph()
            )

    def create_session(self, fake, mentor, mentee):
        future_date = timezone.now() + timedelta(days=random.randint(1, 30))
        session = Session.objects.create(
            mentor=mentor,
            mentee=mentee,
            appointment_id=random.randint(1000, 9999),
            session_topic=fake.catch_phrase(),
            session_duration=random.choice([30, 45, 60, 90]),
            session_notes=fake.text(),
            session_date=future_date
        )
        return session

    def create_payment(self, fake, session, mentee):
        Payment.objects.create(
            mentee=mentee,
            session=session,
            amount=random.randint(50, 500),
            status=random.choice(['pending', 'completed', 'failed'])
        )

    def create_review(self, fake, mentor, mentee, session):
        Review.objects.create(
            mentor=mentor,
            session_id=session.session_id,
            mentee=mentee,
            rating=random.randint(3, 5),
            title_review=fake.sentence(),
            feedback=fake.paragraph()
        )

    def handle(self, *args, **kwargs):
        fake = Faker()

        categories_and_skills = {
            "Computer Science": ["Algorithms", "Data Structures", "Software Development"],
            "System Design": ["Architectural Patterns", "Microservices", "Database Design"],
            "Management": ["Project Management", "Team Leadership"],
            "HR": ["Recruitment", "Employee Relations"],
            "Product Management": ["Product Roadmap", "Feature Prioritization"],
            "User Design": ["UI/UX Design", "Wireframing"],
            "Soft Skills": ["Communication", "Teamwork"],
            "Marketing": ["SEO", "Content Strategy"],
            "Design": ["Graphic Design", "Branding"],
            "Sales": ["Sales Strategy", "Client Relations"],
            "Data Science": ["Machine Learning", "Data Analysis"]
        }

        # Create some mentees first
        mentees = []
        for _ in range(5):
            try:
                username = self.generate_unique_username(fake)
                mentee = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='testpass123'
                )
                mentees.append(mentee)
                self.stdout.write(self.style.SUCCESS(f'Created mentee: {mentee.username}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Error creating mentee: {e}'))

        # Create mentors and related data
        for _ in range(10):
            try:
                # Create mentor user and profile
                username = self.generate_unique_username(fake)
                mentor_user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='testpass123'
                )
                mentor = Mentor.objects.create(
                    user=mentor_user,
                    bio=fake.text(),
                    experience_years=fake.random_int(min=1, max=20),
                    hourly_rate=fake.random_int(min=50, max=500),
                    industry=fake.random_element(list(categories_and_skills.keys())),
                    linkedin_url=fake.url(),
                    education=fake.random_element(["BSc", "MSc", "PhD"])
                )

                # Create availability slots
                self.create_mentor_availability(fake, mentor)

                # Create category and skills
                category_name = fake.random_element(list(categories_and_skills.keys()))
                category = MentorCategory.objects.create(
                    mentor=mentor,
                    category_name=category_name
                )

                # Create skills
                skills = fake.random_elements(
                    elements=categories_and_skills[category_name],
                    length=random.randint(1, len(categories_and_skills[category_name]))
                )
                for skill in skills:
                    MentorSkill.objects.create(
                        mentor=mentor,
                        skill_name=skill,
                        category=category
                    )

                # Create sessions, reviews, and payments with random mentees
                for mentee in random.sample(mentees, random.randint(1, 3)):
                    # Create messages
                    self.create_messages(fake, mentor_user, mentee)

                    # Create session
                    session = self.create_session(fake, mentor, mentee)

                    # Create payment
                    self.create_payment(fake, session, mentee)

                    # Create review (70% chance)
                    if random.random() < 0.7:
                        self.create_review(fake, mentor, mentee, session)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created mentor {mentor_user.username} with complete profile and related data'
                    )
                )

            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Error creating mentor data: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully generated all fake data'))